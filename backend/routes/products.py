from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.database import get_db
from backend.models import Product
from backend.schemas import ProductResponse
from backend.services.recommendations import get_related_products

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("", response_model=List[ProductResponse])
def get_products(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock_only: Optional[bool] = False,
    search: Optional[str] = None,
    sort: Optional[str] = "rating_desc",
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category and category != "All":
        query = query.filter(Product.category == category)

    if brand:
        query = query.filter(Product.brand == brand)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if in_stock_only:
        query = query.filter(Product.stock_quantity > 0)

    if search:
        search_term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.brand.ilike(search_term),
                Product.category.ilike(search_term),
                Product.tags.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )

    # Sorting
    if sort == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort == "rating_desc":
        query = query.order_by(Product.rating.desc())
    elif sort == "newest":
        query = query.order_by(Product.created_at.desc())
    else:
        query = query.order_by(Product.id.asc())

    products = query.all()

    # Decorate with stock badges / why_recommended
    results: List[ProductResponse] = []
    for p in products:
        reasons = []
        if p.stock_quantity > 0:
            reasons.append(f"In stock ({p.stock_quantity} available)")
        else:
            reasons.append("Currently Out of Stock")

        if p.rating >= 4.5:
            reasons.append(f"Customer favorite ({p.rating} ★)")

        results.append(ProductResponse(
            id=p.id,
            name=p.name,
            category=p.category,
            brand=p.brand,
            price=p.price,
            stock_quantity=p.stock_quantity,
            description=p.description,
            rating=p.rating,
            tags=p.tags,
            image_url=p.image_url,
            specs=p.specs,
            created_at=p.created_at,
            why_recommended=reasons
        ))

    return results

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    from sqlalchemy import func
    categories = db.query(Product.category, func.count(Product.id)).group_by(Product.category).all()
    return [{"name": c[0], "count": c[1]} for c in categories]

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    reasons = [
        f"Verified quality from {product.brand}",
        f"Rating: {product.rating} / 5.0 based on real customer reviews",
        f"Live Inventory: {product.stock_quantity} units available" if product.stock_quantity > 0 else "Currently out of stock"
    ]

    return ProductResponse(
        id=product.id,
        name=product.name,
        category=product.category,
        brand=product.brand,
        price=product.price,
        stock_quantity=product.stock_quantity,
        description=product.description,
        rating=product.rating,
        tags=product.tags,
        image_url=product.image_url,
        specs=product.specs,
        created_at=product.created_at,
        why_recommended=reasons
    )

@router.get("/{product_id}/related", response_model=List[ProductResponse])
def get_related(product_id: int, limit: int = 4, db: Session = Depends(get_db)):
    return get_related_products(db, product_id, limit=limit)
