import io
import csv
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database import get_db
from backend.models import Product, Order, OrderItem
from backend.schemas import (
    ProductCreate,
    ProductUpdate,
    ProductStockUpdate,
    ProductResponse,
    AdminDashboardStats,
    AdminAnalyticsResponse,
    TopSellingProduct,
    DailySalesData,
    CSVImportResult
)

router = APIRouter(prefix="/api/admin", tags=["Admin Management"])

@router.get("/dashboard-stats", response_model=AdminDashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Computes real-time admin KPIs:
    - Total Products
    - Total Orders
    - Total Revenue
    - Products Sold (sum of item quantities)
    - Low Stock Products (stock < 5)
    """
    total_products = db.query(Product).count()
    total_orders = db.query(Order).count()

    revenue_query = db.query(func.sum(Order.total_amount)).scalar()
    total_revenue = float(revenue_query) if revenue_query else 0.0

    sold_query = db.query(func.sum(OrderItem.quantity)).scalar()
    products_sold = int(sold_query) if sold_query else 0

    low_stock_count = db.query(Product).filter(Product.stock_quantity < 5).count()

    return AdminDashboardStats(
        total_products=total_products,
        total_orders=total_orders,
        total_revenue=round(total_revenue, 2),
        products_sold=products_sold,
        low_stock_products=low_stock_count
    )

@router.get("/analytics", response_model=AdminAnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    """
    Provides real sales analytics:
    - Revenue & order volume over past 7 days
    - Top selling products ranked by units sold and revenue
    """
    stats = get_dashboard_stats(db)

    # 1. Top selling products
    top_items = (
        db.query(
            OrderItem.product_id,
            OrderItem.product_name,
            func.sum(OrderItem.quantity).label("total_units"),
            func.sum(OrderItem.subtotal).label("total_rev")
        )
        .group_by(OrderItem.product_id, OrderItem.product_name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(6)
        .all()
    )

    top_selling_list: List[TopSellingProduct] = []
    for item in top_items:
        prod = db.query(Product).filter(Product.id == item[0]).first()
        category_name = prod.category if prod else "Electronics"
        top_selling_list.append(TopSellingProduct(
            product_id=item[0],
            product_name=item[1],
            category=category_name,
            units_sold=int(item[2]),
            revenue_generated=round(float(item[3]), 2)
        ))

    # 2. Sales over time (group by date)
    orders = db.query(Order).order_by(Order.created_at.asc()).all()
    date_map: Dict[str, Dict[str, float]] = {}

    # Initialize last 7 days including today
    today = datetime.utcnow().date()
    for i in range(6, -1, -1):
        d_str = (today - timedelta(days=i)).strftime("%b %d")
        date_map[d_str] = {"revenue": 0.0, "orders_count": 0}

    for o in orders:
        if o.created_at:
            d_str = o.created_at.strftime("%b %d")
            if d_str in date_map:
                date_map[d_str]["revenue"] += o.total_amount
                date_map[d_str]["orders_count"] += 1
            else:
                date_map[d_str] = {"revenue": o.total_amount, "orders_count": 1}

    sales_over_time: List[DailySalesData] = []
    for d_str, val in date_map.items():
        sales_over_time.append(DailySalesData(
            date=d_str,
            revenue=round(val["revenue"], 2),
            orders_count=val["orders_count"]
        ))

    return AdminAnalyticsResponse(
        stats=stats,
        sales_over_time=sales_over_time,
        top_selling=top_selling_list
    )

@router.post("/products", response_model=ProductResponse)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    """
    Creates a new product in the catalog.
    """
    new_prod = Product(
        name=payload.name,
        category=payload.category,
        brand=payload.brand,
        price=payload.price,
        stock_quantity=payload.stock_quantity,
        description=payload.description,
        rating=payload.rating,
        tags=payload.tags,
        image_url=payload.image_url,
        specs=payload.specs or "{}"
    )
    db.add(new_prod)
    db.commit()
    db.refresh(new_prod)
    return new_prod

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    """
    Updates product information.
    """
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(prod, field, val)

    db.commit()
    db.refresh(prod)
    return prod

@router.patch("/products/{product_id}/stock", response_model=ProductResponse)
def update_product_stock(product_id: int, payload: ProductStockUpdate, db: Session = Depends(get_db)):
    """
    Fast inline stock updater for inventory management and demo out-of-stock toggling.
    """
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")

    prod.stock_quantity = payload.stock_quantity
    db.commit()
    db.refresh(prod)
    return prod

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(prod)
    db.commit()
    return {"message": f"Product '{prod.name}' deleted successfully", "id": product_id}

@router.get("/sample-csv")
def download_sample_csv():
    """
    Generates and downloads a sample CSV template for bulk product import.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "name", "category", "brand", "price", "stock_quantity",
        "description", "rating", "tags", "image_url"
    ])
    writer.writerow([
        "Lenovo ThinkPad E14 Gen 5", "Laptops", "Lenovo", "62990", "10",
        "Durable business and programming laptop with AMD Ryzen 5, 16GB RAM, 512GB SSD, and legendary ThinkPad keyboard.", "4.6",
        "laptop, coding, programming, lenovo, thinkpad, durable, developer",
        "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=600&auto=format&fit=crop&q=80"
    ])
    writer.writerow([
        "Sony WH-1000XM4 Noise Cancelling", "Headphones", "Sony", "19990", "8",
        "Industry-leading active noise cancellation, 30-hour battery, speak-to-chat, and multipoint Bluetooth connection.", "4.8",
        "headphones, anc, noise cancelling, wireless, sony, audio, premium",
        "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80"
    ])
    output.seek(0)

    response = StreamingResponse(iter([output.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=shopai_products_sample.csv"
    return response

@router.post("/import-csv", response_model=CSVImportResult)
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Parses and imports products from a CSV file into the database.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    content = await file.read()
    try:
        decoded = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        decoded = content.decode("latin-1")

    reader = csv.DictReader(io.StringIO(decoded))
    imported_count = 0
    failed_count = 0
    errors: List[str] = []
    preview: List[Dict[str, Any]] = []

    required_cols = {"name", "category", "brand", "price", "stock_quantity"}

    fieldnames = [f.strip().lower() for f in (reader.fieldnames or [])]
    missing = [c for c in required_cols if c not in fieldnames]
    if missing:
        raise HTTPException(status_code=400, detail=f"CSV missing mandatory columns: {', '.join(missing)}")

    for row_idx, row in enumerate(reader, start=2):
        cleaned_row = {k.strip().lower(): v.strip() for k, v in row.items() if k}
        try:
            name = cleaned_row.get("name")
            category = cleaned_row.get("category", "Accessories")
            brand = cleaned_row.get("brand", "Generic")
            price_val = float(cleaned_row.get("price", 0))
            stock_val = int(cleaned_row.get("stock_quantity", 0))
            desc = cleaned_row.get("description", f"{brand} {name}")
            rating_val = float(cleaned_row.get("rating", 4.0)) if cleaned_row.get("rating") else 4.0
            tags = cleaned_row.get("tags", f"{category}, {brand}")
            img = cleaned_row.get("image_url", "https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=600&auto=format&fit=crop&q=80")

            if not name:
                errors.append(f"Row {row_idx}: Product name cannot be empty.")
                failed_count += 1
                continue

            new_prod = Product(
                name=name,
                category=category,
                brand=brand,
                price=price_val,
                stock_quantity=stock_val,
                description=desc,
                rating=rating_val,
                tags=tags,
                image_url=img,
                specs="{}"
            )
            db.add(new_prod)
            imported_count += 1

            if len(preview) < 5:
                preview.append({
                    "name": name,
                    "category": category,
                    "brand": brand,
                    "price": price_val,
                    "stock_quantity": stock_val
                })
        except Exception as e:
            errors.append(f"Row {row_idx}: Error parsing values ({str(e)})")
            failed_count += 1

    db.commit()

    return CSVImportResult(
        success=True,
        imported_count=imported_count,
        failed_count=failed_count,
        errors=errors[:10],
        sample_preview=preview
    )
