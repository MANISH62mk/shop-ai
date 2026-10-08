import urllib.request
import json
import urllib.parse
import sys

BASE_URL = "http://127.0.0.1:8000"

def safe_str(s):
    if isinstance(s, str):
        return s.replace("\u20b9", "Rs.").replace("\u2605", "*")
    return s

def request_json(path, method="GET", data=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))

def run_tests():
    print("=" * 60)
    print("SHOPAI AUTOMATED SYSTEM VERIFICATION SUITE")
    print("=" * 60)

    # 1. Health check
    health = request_json("/api/health")
    assert health["status"] == "healthy", "Health check failed"
    print("[PASS] Backend Health Check: OK")

    # 2. Auth Login Test
    user_cust = request_json("/api/auth/login", method="POST", data={"email": "demo@shopai.com", "password": "demo123"})
    assert user_cust["email"] == "demo@shopai.com", "Customer login failed"
    print(f"[PASS] Customer Login: OK ({user_cust['name']}, role: {user_cust['role']})")

    user_admin = request_json("/api/auth/login", method="POST", data={"email": "admin@shopai.com", "password": "admin123"})
    assert user_admin["role"] == "admin", "Admin login failed"
    print(f"[PASS] Admin Login: OK ({user_admin['name']}, role: {user_admin['role']})")

    # 3. Product Catalog & Categories
    products = request_json("/api/products")
    assert len(products) >= 30, f"Expected at least 30 products, got {len(products)}"
    print(f"[PASS] Catalog Verification: {len(products)} products active in SQLite")

    categories = request_json("/api/products/categories")
    assert len(categories) >= 7, "Category count mismatch"
    print(f"[PASS] Category Breakdown: {len(categories)} categories verified")

    # 4. Phase 11 Core Natural Language Query Test
    test_query = "I need a lightweight laptop for coding under 60000"
    ai_search = request_json("/api/ai/search", method="POST", data={"query": test_query})
    print("\n--- AI SEMANTIC SEARCH TEST ---")
    print(f"Query: '{test_query}'")
    print(f"Extracted Category: {ai_search['extracted_intent']['category']}")
    print(f"Extracted Max Budget: {ai_search['extracted_intent']['max_budget']}")
    print(f"Extracted Use Case: {ai_search['extracted_intent']['use_case']}")
    print(f"AI Message: {safe_str(ai_search['response_message'])}")
    print(f"Found In-Stock Matches: {ai_search['total_found']}")
    assert ai_search["total_found"] > 0, "No products found for query"
    top_laptop = ai_search["products"][0]
    print(f"Top Recommended Laptop: '{top_laptop['name']}' (Rs. {top_laptop['price']:,})")
    print("Why Recommended Reasons:")
    for r in top_laptop["why_recommended"]:
        print(f"  - {safe_str(r)}")
    assert top_laptop["price"] <= 60000, "Recommended laptop exceeds 60,000 budget"

    # 5. Out of Stock alternative test
    print("\n--- OUT-OF-STOCK ALTERNATIVE RECOMMENDATION TEST ---")
    oos_search = request_json("/api/ai/search", method="POST", data={"query": "Acer Aspire 5"})
    print(f"Query: 'Acer Aspire 5'")
    print(f"Out of Stock Notice: {safe_str(oos_search['out_of_stock_alert'])}")
    assert oos_search["out_of_stock_alert"] is not None, "Expected out of stock alert"
    assert oos_search["total_found"] > 0, "Expected in-stock alternatives"
    print(f"Offered {oos_search['total_found']} available alternatives! Top alternative: {oos_search['products'][0]['name']}")

    # 6. Cart and Stock Decrement End-to-End Flow
    print("\n--- CART & CHECKOUT END-TO-END FLOW ---")
    session_id = "test_e2e_session_99"

    # Clear test cart first
    request_json(f"/api/cart?session_id={session_id}", method="DELETE")

    # Pick top laptop
    laptop_id = top_laptop["id"]
    initial_stock = top_laptop["stock_quantity"]
    print(f"Selected: '{top_laptop['name']}' (ID: {laptop_id})")
    print(f"Initial Live Stock: {initial_stock}")

    # Add 1 unit to cart
    cart = request_json("/api/cart", method="POST", data={"product_id": laptop_id, "quantity": 1, "session_id": session_id})
    assert cart["item_count"] == 1, "Cart item count should be 1"
    print(f"[PASS] Added 1 unit to Cart. Subtotal: Rs. {cart['subtotal']:,}")

    # Test stock limit enforcement (attempt to add 9999 units)
    try:
        request_json("/api/cart", method="POST", data={"product_id": laptop_id, "quantity": 9999, "session_id": session_id})
        assert False, "Should have thrown stock limit exceeded error"
    except urllib.error.HTTPError as e:
        assert e.code == 400, "Expected 400 error for exceeding stock"
        print("[PASS] Inventory Safeguard: Successfully blocked adding quantity exceeding stock")

    # Place Demo Order
    checkout_payload = {
        "session_id": session_id,
        "customer_name": "Kavya Patel",
        "customer_email": "kavya@example.com",
        "customer_phone": "+91 9988776655",
        "shipping_address": "Flat 304, Sapphire Enclave, Indiranagar, Bengaluru, KA 560038",
        "payment_method": "Demo Card Payment"
    }
    order = request_json("/api/orders/checkout", method="POST", data=checkout_payload)
    print(f"[PASS] Placed Demo Order: #ORD-{order['id']} (Amount: Rs. {order['total_amount']:,})")

    # Verify Stock Decremented by 1
    updated_prod = request_json(f"/api/products/{laptop_id}")
    new_stock = updated_prod["stock_quantity"]
    print(f"Stock after checkout: {new_stock} (Expected: {initial_stock - 1})")
    assert new_stock == initial_stock - 1, f"Stock did not decrement correctly! Initial: {initial_stock}, New: {new_stock}"
    print("[PASS] Stock Automatic Decrement Verified: SUCCESS!")

    # Verify Cart Cleared
    cart_after = request_json(f"/api/cart?session_id={session_id}")
    assert cart_after["item_count"] == 0, "Cart should be empty after checkout"
    print("[PASS] Cart auto-cleared after checkout: OK")

    # 7. Admin Dashboard and Analytics
    print("\n--- ADMIN DASHBOARD & ANALYTICS VERIFICATION ---")
    admin_stats = request_json("/api/admin/dashboard-stats")
    print(f"Total Products: {admin_stats['total_products']}")
    print(f"Total Orders: {admin_stats['total_orders']}")
    print(f"Total Revenue: Rs. {admin_stats['total_revenue']:,}")
    print(f"Products Sold: {admin_stats['products_sold']}")
    print(f"Low Stock Count: {admin_stats['low_stock_products']}")
    assert admin_stats["total_orders"] >= 3, "Orders count should include newly placed order"
    print("[PASS] Admin KPIs live update: SUCCESS")

    # 8. CSV Sample download check
    sample_csv = urllib.request.urlopen(f"{BASE_URL}/api/admin/sample-csv").read().decode()
    assert "name,category,brand,price" in sample_csv, "Sample CSV invalid"
    print("[PASS] Sample CSV format generation: OK")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
