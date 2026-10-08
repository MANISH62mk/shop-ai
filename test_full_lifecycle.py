import uuid
from backend.database import SessionLocal
from backend.models import Product, Order, OrderItem, CartItem
from backend.services.ai_search import perform_ai_semantic_search
from backend.routes.cart import add_to_cart, get_cart
from backend.routes.orders import checkout_cart
from backend.schemas import CartItemCreate, CheckoutRequest

def test_full_flow():
    db = SessionLocal()
    print("=" * 70)
    print("RUNNING END-TO-END VALIDATION ACROSS MULTIPLE CATEGORIES")
    print("=" * 70)

    test_queries = [
        ("Cotton shirt under Rs.1,500", "Clothing", 1500.0),
        ("Double door refrigerator under Rs.40,000", "Refrigerators", 40000.0),
        ("Running shoes under Rs.3,000", "Shoes", 3000.0),
        ("Office chair under Rs.8,000", "Furniture", 8000.0),
    ]

    for q_text, expected_cat, max_p in test_queries:
        print(f"\n--- Testing flow for: '{q_text}' ---")
        search_res = perform_ai_semantic_search(db, q_text)
        assert search_res.total_found > 0, f"No products found for {q_text}"
        product = search_res.products[0]
        print(f"1. AI recommended: '{product.name}' ({product.category})")
        print(f"   Price: Rs.{product.price:,.0f} | Stock: {product.stock_quantity}")
        if product.why_recommended:
            print(f"   Why recommended: {product.why_recommended[0].replace('\u20b9', 'Rs.')}")

        # Check constraints
        assert product.category == expected_cat, f"Category mismatch: {product.category} != {expected_cat}"
        if max_p:
            assert product.price <= max_p, f"Budget exceeded: {product.price} > {max_p}"
        assert product.stock_quantity > 0, f"Stock invalid: {product.stock_quantity}"

        initial_stock = product.stock_quantity
        session_id = f"test-session-{uuid.uuid4().hex[:8]}"

        # 2. Add to Cart
        cart_req = CartItemCreate(
            product_id=product.id,
            quantity=1,
            session_id=session_id
        )
        cart_res = add_to_cart(cart_req, db=db)
        print(f"2. Added to cart! Items in cart: {cart_res.item_count}, Total: Rs.{cart_res.total:,.0f}")
        assert cart_res.item_count == 1
        assert cart_res.subtotal == product.price

        # 3. Checkout
        checkout_req = CheckoutRequest(
            session_id=session_id,
            customer_name="Test Customer",
            customer_email="test@shopai.internal",
            customer_phone="+91 9999999999",
            shipping_address="123 AI Street, Tech City, 560001",
            payment_method="Cash on Delivery"
        )
        order = checkout_cart(checkout_req, db=db)
        print(f"3. Checkout successful! Order #{order.id} placed, Status: {order.status}")
        assert order.status == "Confirmed"
        assert len(order.items) == 1
        assert order.items[0].product_id == product.id

        # 4. Verify Stock decrement
        db_prod = db.query(Product).filter(Product.id == product.id).first()
        print(f"4. Stock before: {initial_stock} -> Stock after checkout: {db_prod.stock_quantity}")
        assert db_prod.stock_quantity == initial_stock - 1, f"Stock did not decrement correctly! {db_prod.stock_quantity} != {initial_stock - 1}"
        print(f"   [PASS] Stock atomically decremented by 1.")

    db.close()
    print("\n" + "=" * 70)
    print("ALL MULTI-CATEGORY CART & CHECKOUT FLOWS PASSED PERFECTLY!")
    print("=" * 70)

if __name__ == "__main__":
    test_full_flow()
