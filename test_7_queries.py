import sqlite3
from backend.database import SessionLocal
from backend.services.ai_search import perform_ai_semantic_search

TEST_QUERIES = [
    ("Laptop for coding under \u20b960,000", "Laptops", 60000.0),
    ("Cotton shirt under \u20b91,500", "Clothing", 1500.0),
    ("Double door refrigerator under \u20b940,000", "Refrigerators", 40000.0),
    ("Running shoes under \u20b93,000", "Shoes", 3000.0),
    ("Smartphone with good camera under \u20b930,000", "Smartphones", 30000.0),
    ("Gaming headphones", "Headphones", None),
    ("Office chair under \u20b98,000", "Furniture", 8000.0),
]

def run():
    db = SessionLocal()
    print("=" * 70)
    print("VERIFYING 7 USER QUERIES ON GENERAL E-COMMERCE AI ENGINE")
    print("=" * 70)

    all_passed = True
    for query, expected_cat, max_budget in TEST_QUERIES:
        res = perform_ai_semantic_search(db, query)
        detected_cat = res.extracted_intent.category
        budget_detected = res.extracted_intent.max_budget
        found = res.total_found

        safe_query = query.replace("\u20b9", "Rs.")
        print(f"\nQUERY: \"{safe_query}\"")
        print(f"  -> Detected Category: {detected_cat} (Expected: {expected_cat})")
        print(f"  -> Detected Budget:   {budget_detected} (Expected: {max_budget})")
        print(f"  -> In-Stock Found:    {found}")

        if detected_cat != expected_cat:
            print(f"  [FAIL] Category mismatch!")
            all_passed = False
            continue

        if found == 0:
            print(f"  [FAIL] Zero products found!")
            all_passed = False
            continue

        # Check all returned products
        price_violation = False
        stock_violation = False
        cat_violation = False

        for p in res.products:
            if max_budget is not None and p.price > max_budget:
                price_violation = True
                print(f"  [FAIL] Hard budget violated: {p.name} costs Rs.{p.price} > {max_budget}")
            if p.stock_quantity <= 0:
                stock_violation = True
                print(f"  [FAIL] Out of stock item shown: {p.name}")
            if p.category != expected_cat:
                cat_violation = True
                print(f"  [FAIL] Wrong category product: {p.name} ({p.category})")

        if price_violation or stock_violation or cat_violation:
            all_passed = False
            continue

        print(f"  [PASS] Top 2 products:")
        for p in res.products[:2]:
            print(f"     * {p.name} | Rs.{p.price:,.0f} | Stock: {p.stock_quantity} | Match: {p.relevance_score}%")
            if p.why_recommended:
                safe_r = p.why_recommended[0].replace("\u20b9", "Rs.")
                print(f"       Reason: {safe_r}")

    db.close()
    print("\n" + "=" * 70)
    if all_passed:
        print("ALL 7 CORE SEARCH QUERIES PASSED WITH 100% ACCURACY!")
    else:
        print("SOME CHECKS FAILED.")
    print("=" * 70)

if __name__ == "__main__":
    run()
