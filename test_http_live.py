import urllib.request
import json

queries = [
    ("Laptop for coding under 60000", "Laptops", 60000),
    ("Cotton shirt under 1500", "Clothing", 1500),
    ("Double door refrigerator under 40000", "Refrigerators", 40000),
    ("Running shoes under 3000", "Shoes", 3000),
    ("Smartphone with good camera under 30000", "Smartphones", 30000),
    ("Gaming headphones", "Headphones", None),
    ("Office chair under 8000", "Furniture", 8000)
]

print("=" * 80)
print("TESTING 7 QUERIES OVER LIVE HTTP SERVER (http://127.0.0.1:8000)")
print("=" * 80)

for q, expected_cat, expected_budget in queries:
    req = urllib.request.Request(
        'http://127.0.0.1:8000/api/ai/search',
        data=json.dumps({'query': q}).encode(),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as r:
        d = json.loads(r.read().decode())
        det_cat = d["extracted_intent"]["category"]
        found = d["total_found"]
        top_name = d["products"][0]["name"] if d["products"] else "None"
        top_price = d["products"][0]["price"] if d["products"] else 0
        print(f"[{det_cat}] {q}")
        print(f"   -> Top: {top_name} (Rs.{top_price:,.0f}) | Total in-stock: {found}")
        assert det_cat == expected_cat
        assert found > 0
        if expected_budget:
            assert top_price <= expected_budget

print("=" * 80)
print("ALL 7 QUERIES VERIFIED OVER LIVE HTTP REST API!")
print("=" * 80)
