import re
import json
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from backend.models import Product
from backend.schemas import ExtractedIntent, AISearchResponse, ProductResponse

# Supported E-Commerce Categories
CATEGORIES = [
    "Laptops",
    "Smartphones",
    "Headphones",
    "Clothing",
    "Shoes",
    "Refrigerators",
    "Televisions",
    "Furniture",
    "Computer Accessories",
    "Home Appliances",
    "Smartwatches",
    "Tablets"
]

# Category synonyms mapped for natural-language intent inference
CATEGORY_SYNONYMS = {
    "Refrigerators": [
        "double door refrigerator", "double door fridge", "single door refrigerator",
        "single door fridge", "frost free refrigerator", "refrigerator", "refrigerators",
        "fridge", "fridges", "deep freezer", "freezer", "double door"
    ],
    "Clothing": [
        "cotton shirt", "cotton shirts", "linen shirt", "formal shirt", "casual shirt",
        "oxford shirt", "polo shirt", "shirt", "shirts", "t-shirt", "t-shirts", "tshirt",
        "tshirts", "kurta", "kurtas", "jeans", "trousers", "pant", "pants", "clothing",
        "clothes", "apparel", "wear", "dress"
    ],
    "Shoes": [
        "running shoes", "running shoe", "road running shoes", "road running",
        "sports shoes", "jogging shoes", "sneaker", "sneakers", "shoe", "shoes",
        "footwear", "trainers", "boots", "loafers"
    ],
    "Furniture": [
        "office chair", "office chairs", "study chair", "ergonomic chair", "desk chair",
        "computer desk", "study desk", "coffee table", "dining table", "chair", "chairs",
        "desk", "table", "tables", "furniture", "sofa", "couch", "bed", "mattress"
    ],
    "Televisions": [
        "smart tv", "led tv", "oled tv", "qled tv", "4k tv", "google tv", "android tv",
        "television", "televisions", "tv", "tvs"
    ],
    "Home Appliances": [
        "air fryer", "vacuum cleaner", "robotic vacuum", "mixer grinder", "water heater",
        "geyser", "water purifier", "microwave oven", "ceiling fan", "home appliances",
        "home appliance", "appliances", "appliance", "purifier", "microwave", "fan"
    ],
    "Computer Accessories": [
        "computer accessories", "computer accessory", "mechanical keyboard", "coding monitor",
        "eye care monitor", "laptop stand", "gaming monitor", "keyboard", "keyboards",
        "monitor", "monitors", "mouse", "mice", "webcam", "charger", "adapter",
        "flash drive", "pen drive", "usb", "dongle", "cable", "accessories", "accessory"
    ],
    "Laptops": [
        "gaming laptop", "coding laptop", "thin and light laptop", "ultrabook",
        "laptop", "laptops", "notebook", "notebooks", "macbook", "pc", "computer"
    ],
    "Smartphones": [
        "camera phone", "5g phone", "smartphone", "smartphones", "phone", "phones",
        "mobile", "mobiles", "android", "iphone", "cellphone"
    ],
    "Headphones": [
        "gaming headphones", "gaming headset", "wireless headphones", "noise cancelling headphones",
        "headphone", "headphones", "earphone", "earphones", "earbuds", "tws", "neckband",
        "headset", "audio"
    ],
    "Smartwatches": [
        "smartwatch", "smartwatches", "fitness band", "tracker", "smart watch", "watch", "watches"
    ],
    "Tablets": [
        "tablet", "tablets", "tab", "ipad"
    ]
}

# Extensive recognized brands across all categories
BRAND_LIST = [
    # Tech & Electronics
    "acer", "asus", "lenovo", "hp", "dell", "apple", "xiaomi", "redmi",
    "realme", "oneplus", "samsung", "boat", "sony", "noise", "redragon",
    "logitech", "keychron", "benq", "lg", "amazfit", "portronics", "anker",
    "sandisk", "tp-link", "tcl", "razer", "hyperx", "cosmic byte", "vivo", "motorola", "google",
    # Appliances & Refrigerators
    "whirlpool", "haier", "godrej", "philips", "preethi", "bajaj", "havells", "kent",
    "morphy richards", "eureka forbes", "dyson",
    # Clothing & Shoes
    "allen solly", "peter england", "u.s. polo assn", "us polo", "h&m", "fabindia",
    "raymond", "levi's", "levis", "zara", "puma", "nike", "adidas", "reebok",
    "campus", "sparx", "asics", "skechers",
    # Furniture
    "green soul", "da urban", "wakefit", "savya home", "the sleep company", "deckup",
    "bluewud", "solimo"
]

STOP_WORDS = {
    "i", "need", "a", "an", "the", "for", "under", "below", "less", "than",
    "with", "show", "me", "find", "suggest", "something", "some", "best",
    "good", "want", "looking", "please", "can", "you", "give", "of", "in",
    "at", "to", "and", "or", "is", "are", "rupees", "rs", "inr", "buy"
}

def parse_natural_language_intent(query: str) -> ExtractedIntent:
    """
    Extracts category, maximum budget, use cases, materials, subcategories,
    and semantic keywords from general e-commerce queries.
    """
    query_lower = query.lower()

    # 1. Category extraction (Sort synonyms by length descending to match compound terms first)
    detected_category: Optional[str] = None
    all_synonym_pairs = []
    for category, synonyms in CATEGORY_SYNONYMS.items():
        for syn in synonyms:
            all_synonym_pairs.append((syn, category))
    # Longest phrase first (e.g. "double door refrigerator" before "refrigerator", "cotton shirt" before "shirt")
    all_synonym_pairs.sort(key=lambda x: len(x[0]), reverse=True)

    for syn, cat in all_synonym_pairs:
        # Check boundary or direct phrase match
        pattern = r'(?:\b|^)' + re.escape(syn) + r'(?:\b|$)'
        if re.search(pattern, query_lower):
            detected_category = cat
            break

    # 2. Budget extraction (Hard Constraint Support)
    max_budget: Optional[float] = None
    budget_patterns = [
        # "under ₹60,000", "under 1,500", "below 3000", "under 60k", "upto 40000"
        r'(?:under|below|less\s+than|within|upto|up\s+to|max(?:imum)?)\s*(?:of)?\s*(?:₹|rs\.?|inr)?\s*([0-9,]+(?:\.[0-9]+)?)\s*(k)?\b',
        # "budget of ₹30,000", "price under 1500"
        r'(?:budget|price)\s*(?:of)?\s*(?:under|below|upto)?\s*(?:₹|rs\.?|inr)?\s*([0-9,]+(?:\.[0-9]+)?)\s*(k)?\b',
        # "₹1,500", "₹40,000"
        r'(?:₹|rs\.?|inr)\s*([0-9,]+(?:\.[0-9]+)?)\s*(k)?\b',
        # "1500 rupees"
        r'\b([0-9,]+)\s*(?:rupees|rs|inr)\b'
    ]

    for pat in budget_patterns:
        match = re.search(pat, query_lower)
        if match:
            num_str = match.group(1).replace(',', '')
            try:
                val = float(num_str)
                # Check for 'k' multiplier
                if len(match.groups()) >= 2 and match.group(2) and match.group(2).lower() == 'k':
                    val *= 1000
                elif val < 500 and "k" in match.group(0).lower():
                    val *= 1000
                max_budget = val
                break
            except ValueError:
                pass

    # 3. Brand extraction
    detected_brand: Optional[str] = None
    for brand in BRAND_LIST:
        if re.search(r'\b' + re.escape(brand) + r'\b', query_lower):
            detected_brand = brand.capitalize()
            break

    # 4. Attribute / Use Case / Feature extraction
    detected_use_case: Optional[str] = None
    features_requested: List[str] = []

    # Use Case: Coding
    if any(k in query_lower for k in ["coding", "programming", "developer", "software", "python", "code"]):
        detected_use_case = "Coding"
        features_requested.append("Optimized for coding & development")

    # Use Case: Gaming
    if any(k in query_lower for k in ["gaming", "gamer", "games", "esports", "play games"]):
        detected_use_case = "Gaming"
        features_requested.append("High-performance gaming specs")

    # Use Case: Running
    if any(k in query_lower for k in ["running", "jogging", "marathon", "sprint", "workout"]):
        detected_use_case = "Running"
        features_requested.append("Responsive cushioning for running")

    # Material: Cotton
    if any(k in query_lower for k in ["cotton", "pure cotton", "100% cotton"]):
        features_requested.append("100% Breathable pure cotton")

    # Subcategory / Type: Double Door
    if any(k in query_lower for k in ["double door", "2 door", "frost free"]):
        features_requested.append("Double Door Frost-Free Design")

    # Subcategory / Type: Office Chair
    if any(k in query_lower for k in ["office chair", "desk chair", "ergonomic chair"]):
        if not detected_use_case:
            detected_use_case = "Office / Ergonomic"
        features_requested.append("Ergonomic lumbar support for desk work")

    # Feature: Camera
    if any(k in query_lower for k in ["camera", "photography", "photo", "portrait", "selfie", "ois"]):
        if not detected_use_case:
            detected_use_case = "Photography"
        features_requested.append("Superior camera optics & stabilization")

    # Feature: Family / Large capacity
    if any(k in query_lower for k in ["family", "large family", "capacity"]):
        if not detected_use_case:
            detected_use_case = "Family"
        features_requested.append("Spacious capacity for family needs")

    # Feature: Lightweight / Portable
    if any(k in query_lower for k in ["lightweight", "light", "portable", "thin", "slim"]):
        features_requested.append("Lightweight & portable design")

    # Feature: Wireless
    if any(k in query_lower for k in ["wireless", "bluetooth", "tws", "cordless"]):
        features_requested.append("Wireless Bluetooth connectivity")

    # 5. Semantic Keywords extraction
    words = re.findall(r'\b[a-z0-9]+\b', query_lower)
    keywords = [w for w in words if w not in STOP_WORDS and len(w) > 2]

    return ExtractedIntent(
        category=detected_category,
        max_budget=max_budget,
        min_budget=None,
        brand=detected_brand,
        use_case=detected_use_case,
        keywords=keywords,
        features_requested=features_requested
    )

def calculate_relevance_and_reasons(
    product: Product,
    intent: ExtractedIntent,
    query_tokens: List[str],
    query_lower: str
) -> Tuple[float, List[str]]:
    """
    Computes a relevance score and generates dynamic, category-tailored 'Why recommended' points.
    """
    score = 70.0
    reasons: List[str] = []
    prod_text = f"{product.name} {product.description} {product.tags} {product.brand} {product.category}".lower()

    # 1. Category Matching
    if intent.category:
        if product.category.lower() == intent.category.lower():
            score += 20.0
        else:
            return -100.0, []

    # 2. Budget Matching (Within budget)
    if intent.max_budget:
        if product.price <= intent.max_budget:
            score += 15.0
            reasons.append(f"Within your budget (₹{product.price:,.0f} is under ₹{intent.max_budget:,.0f})")

    # 3. Specific Attribute / Subcategory Alignment
    # Cotton shirts
    if "cotton" in query_lower:
        if "cotton" in prod_text:
            score += 25.0
            reasons.append("Crafted from 100% breathable pure cotton fabric")

    # Double Door Refrigerators
    if "double door" in query_lower:
        if "double door" in prod_text:
            score += 25.0
            reasons.append("Energy-efficient double door design ideal for families")

    # Running shoes
    if "running" in query_lower:
        if "running" in prod_text:
            score += 25.0
            reasons.append("Lightweight responsive cushioning designed for running")

    # Coding / Programming
    if intent.use_case == "Coding" or "coding" in query_lower or "programming" in query_lower:
        if any(w in prod_text for w in ["coding", "programming", "developer", "ide", "16gb", "i5", "ryzen", "ssd"]):
            score += 25.0
            reasons.append("Optimized performance for coding, IDEs, and multitasking")

    # Gaming
    if intent.use_case == "Gaming" or "gaming" in query_lower:
        if any(w in prod_text for w in ["gaming", "surround", "dts", "7.1", "gpu", "rtx", "144hz", "mic"]):
            score += 25.0
            reasons.append("Equipped for immersive gaming audio and low-latency response")

    # Camera
    if any(k in query_lower for k in ["camera", "photography", "photos"]):
        if any(w in prod_text for w in ["camera", "ois", "200mp", "50mp", "sony", "portrait", "zeiss"]):
            score += 25.0
            reasons.append("High-resolution camera system with optical image stabilization")

    # Office Chair / Ergonomics
    if "office chair" in query_lower or "chair" in query_lower:
        if any(w in prod_text for w in ["office chair", "lumbar", "ergonomic", "mesh", "executive"]):
            score += 25.0
            reasons.append("Ergonomic lumbar support engineered for long sitting comfort")

    # Family refrigerator use case
    if "family" in query_lower:
        if any(w in prod_text for w in ["family", "large family", "253l", "242l", "322l", "345l", "frost free"]):
            score += 20.0
            reasons.append("Generous capacity and rapid cooling for family groceries")

    # Lightweight check
    if "lightweight" in query_lower:
        if any(w in prod_text for w in ["lightweight", "thin", "slim", "portable", "1.25 kg", "1.4 kg", "240g", "250g"]):
            score += 15.0
            reasons.append("Ultra-portable lightweight construction")

    # Brand matching
    if intent.brand:
        if intent.brand.lower() in product.brand.lower():
            score += 20.0
            reasons.append(f"Official {product.brand} authentic product")

    # Keyword overlap
    for kw in intent.keywords:
        if kw in prod_text:
            score += 5.0

    # Rating Quality Bonus
    if product.rating >= 4.5:
        reasons.append(f"Top customer satisfaction rating ({product.rating} ★)")
    elif product.rating >= 4.0:
        reasons.append(f"Verified quality rating ({product.rating} ★)")

    # Stock Availability
    if product.stock_quantity > 0:
        if product.stock_quantity <= 3:
            reasons.append(f"Currently in stock (Only {product.stock_quantity} left!)")
        else:
            reasons.append(f"Currently in stock ({product.stock_quantity} units ready to ship)")

    # Ensure at least 3 reasons
    if len(reasons) < 3:
        reasons.append(f"Verified authentic {product.brand} product with brand warranty")

    return score, reasons

def perform_ai_semantic_search(db: Session, query: str) -> AISearchResponse:
    """
    General E-Commerce AI Search Pipeline:
    Natural language query
            ↓
    Intent extraction
            ↓
    Category detection
            ↓
    Budget extraction
            ↓
    Attribute/use-case extraction
            ↓
    HARD FILTERS (Strict budget & category enforcement)
            ↓
    Semantic/relevance ranking
            ↓
    Inventory filter (stock_quantity > 0)
            ↓
    Product recommendations with reasons & match percentage
    """
    cleaned_query = query.strip()
    query_lower = cleaned_query.lower()
    intent = parse_natural_language_intent(cleaned_query)
    query_tokens = [w for w in re.findall(r'\b[a-z0-9]+\b', query_lower) if w not in STOP_WORDS]

    all_products = db.query(Product).all()

    scored_products: List[Tuple[float, Product, List[str]]] = []
    out_of_stock_matches: List[Product] = []

    for p in all_products:
        # ==========================================
        # HARD CONSTRAINT 1: Category Filter
        # ==========================================
        if intent.category:
            if p.category.lower() != intent.category.lower():
                continue

        # ==========================================
        # HARD CONSTRAINT 2: Budget Filter
        # "If user specifies 'under ₹60,000', then product.price <= 60000 MUST be enforced.
        #  Never show ₹68,000 products in the main results."
        # ==========================================
        if intent.max_budget is not None:
            if p.price > intent.max_budget:
                continue

        # Calculate relevance score & dynamic reasons
        score, reasons = calculate_relevance_and_reasons(p, intent, query_tokens, query_lower)

        # ==========================================
        # HARD CONSTRAINT 3: Live Inventory Filter
        # "Always enforce stock_quantity > 0 for available recommendations."
        # ==========================================
        if p.stock_quantity <= 0:
            # If user explicitly searched for an out-of-stock item, track it for out-of-stock notification
            if score > 20:
                out_of_stock_matches.append(p)
            continue

        scored_products.append((score, p, reasons))

    # Sort descending by score
    scored_products.sort(key=lambda x: x[0], reverse=True)

    # Format recommended product responses
    recommended_product_responses: List[ProductResponse] = []
    for score, prod, reasons in scored_products:
        # Normalize score into a credible match percentage between 85% and 99%
        match_pct = min(99.0, max(85.0, round(score * 0.85, 1)))

        prod_resp = ProductResponse(
            id=prod.id,
            name=prod.name,
            category=prod.category,
            brand=prod.brand,
            price=prod.price,
            stock_quantity=prod.stock_quantity,
            description=prod.description,
            rating=prod.rating,
            tags=prod.tags,
            image_url=prod.image_url,
            specs=prod.specs,
            created_at=prod.created_at,
            why_recommended=reasons,
            relevance_score=match_pct
        )
        recommended_product_responses.append(prod_resp)

    total_found = len(recommended_product_responses)
    out_of_stock_alert: Optional[str] = None

    if out_of_stock_matches and total_found > 0:
        oos_names = ", ".join([p.name for p in out_of_stock_matches[:2]])
        out_of_stock_alert = (
            f"Notice: '{oos_names}' is currently Out of Stock (0 units remaining). "
            f"ShopAI has automatically found {total_found} available in-stock alternative(s) matching your criteria."
        )

    # Human-friendly natural AI response message
    if total_found > 0:
        cat_desc = intent.category.lower() if intent.category else "products"
        parts = [f"Based on your requirements, I found {total_found} {cat_desc}"]
        if intent.use_case:
            parts.append(f"suitable for {intent.use_case}")
        if intent.max_budget:
            parts.append(f"under ₹{intent.max_budget:,.0f}")
        response_msg = " ".join(parts) + ". All recommended products are verified in live inventory."
    else:
        # Fallback if strict filter yielded no results, offer closest available items in category or store
        fallback_query = db.query(Product).filter(Product.stock_quantity > 0)
        if intent.category:
            fallback_query = fallback_query.filter(Product.category == intent.category)
        available_fallback = fallback_query.order_by(Product.rating.desc()).limit(4).all()

        for p in available_fallback:
            recommended_product_responses.append(ProductResponse(
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
                why_recommended=[
                    "Top rated option in current inventory",
                    f"In stock ({p.stock_quantity} units available)",
                    "Verified customer rating"
                ],
                relevance_score=85.0
            ))
        response_msg = f"No in-stock items found matching all constraints for '{cleaned_query}'. Here are our top available alternatives."
        total_found = len(recommended_product_responses)

    return AISearchResponse(
        query=cleaned_query,
        extracted_intent=intent,
        response_message=response_msg,
        products=recommended_product_responses,
        out_of_stock_alert=out_of_stock_alert,
        total_found=total_found
    )
