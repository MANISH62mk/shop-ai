from backend.database import SessionLocal
from backend.routes.products import get_products
from backend.routes.admin import create_product, update_product_stock, delete_product
from backend.schemas import ProductCreate, ProductStockUpdate

def test_admin():
    db = SessionLocal()
    print("=" * 70)
    print("VERIFYING CATEGORY-INDEPENDENT ADMIN CAPABILITIES")
    print("=" * 70)

    # 1. Filter by category
    all_clothing = get_products(category="Clothing", db=db)
    print(f"1. Catalog filter for 'Clothing': {len(all_clothing)} items found.")
    assert len(all_clothing) >= 8

    all_fridges = get_products(category="Refrigerators", db=db)
    print(f"   Catalog filter for 'Refrigerators': {len(all_fridges)} items found.")
    assert len(all_fridges) >= 8

    # 2. Admin adds a new product in Home Appliances
    new_prod_payload = ProductCreate(
        name="Philips Air Fryer HD9252",
        category="Home Appliances",
        brand="Philips",
        price=7999.0,
        stock_quantity=15,
        description="Rapid Air Technology air fryer for healthy oil-free cooking.",
        rating=4.7,
        tags="air fryer, philips, kitchen, appliance, cooking",
        image_url="https://images.unsplash.com/photo-1586208958839-06c17cacdf08?w=600&auto=format&fit=crop&q=80",
        specs='{"Capacity": "4.1 Litres", "Power": "1400W"}'
    )
    created = create_product(new_prod_payload, db=db)
    print(f"2. Admin created product: id={created.id}, name='{created.name}', category='{created.category}', stock={created.stock_quantity}")
    assert created.id is not None
    assert created.category == "Home Appliances"

    # 3. Update stock
    updated = update_product_stock(created.id, ProductStockUpdate(stock_quantity=25), db=db)
    print(f"3. Admin updated stock for id={created.id}: new stock={updated.stock_quantity}")
    assert updated.stock_quantity == 25

    # 4. Clean up test product
    delete_product(created.id, db=db)
    print(f"4. Admin deleted test product id={created.id}.")

    db.close()
    print("\n" + "=" * 70)
    print("ADMIN MULTI-CATEGORY MANAGEMENT PASSED COMPLETELY!")
    print("=" * 70)

if __name__ == "__main__":
    test_admin()
