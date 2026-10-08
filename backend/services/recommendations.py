from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models import Product, Order, OrderItem
from backend.schemas import ProductResponse

def get_recommendations_for_user(
    db: Session,
    viewed_product_ids: Optional[List[int]] = None,
    preferred_category: Optional[str] = None,
    user_id: Optional[int] = None,
    limit: int = 6
) -> List[ProductResponse]:
    """
    Intelligent recommendation engine taking into account:
    - Products in stock only (stock_quantity > 0)
    - Categories from previously viewed products
    - User past purchase history (if logged in)
    - Overall product rating & popularity (units sold in OrderItem)
    """
    # 1. Gather historical categories or brands from user orders
    target_categories = set()
    if preferred_category:
        target_categories.add(preferred_category)

    if user_id:
        user_orders = db.query(Order).filter(Order.user_id == user_id).all()
        for o in user_orders:
            for item in o.items:
                if item.product:
                    target_categories.add(item.product.category)

    # 2. Gather categories from viewed products
    if viewed_product_ids:
        viewed_prods = db.query(Product).filter(Product.id.in_(viewed_product_ids)).all()
        for vp in viewed_prods:
            target_categories.add(vp.category)

    # 3. Compute popularity counts per product from order items
    popularity_subquery = (
        db.query(OrderItem.product_id, func.sum(OrderItem.quantity).label("units_sold"))
        .group_by(OrderItem.product_id)
        .subquery()
    )

    query = (
        db.query(Product, func.coalesce(popularity_subquery.c.units_sold, 0).label("sold"))
        .outerjoin(popularity_subquery, Product.id == popularity_subquery.c.product_id)
        .filter(Product.stock_quantity > 0) # STRICTLY in-stock products only
    )

    # Exclude already viewed products if we have plenty of alternatives
    if viewed_product_ids and len(viewed_product_ids) < 10:
        query = query.filter(~Product.id.in_(viewed_product_ids))

    all_candidate_tuples = query.all()

    # Score each candidate:
    # Score = Category affinity (30) + Rating (x8) + Popularity (x5) + In-stock (10)
    scored: List[tuple] = []
    for prod, units_sold in all_candidate_tuples:
        score = 0.0
        reasons: List[str] = []

        if prod.category in target_categories:
            score += 35.0
            reasons.append(f"Matches your interest in {prod.category}")

        if units_sold > 0:
            score += min(float(units_sold) * 6.0, 30.0)
            reasons.append(f"Trending choice ({int(units_sold)} recently ordered)")

        if prod.rating >= 4.5:
            score += prod.rating * 5.0
            reasons.append(f"Top-rated by customers ({prod.rating} ★)")
        else:
            score += prod.rating * 3.0

        if prod.stock_quantity > 0:
            reasons.append(f"Live in stock ({prod.stock_quantity} units ready to ship)")

        if len(reasons) < 2:
            reasons.append("Staff pick recommendation")

        scored.append((score, prod, reasons))

    scored.sort(key=lambda x: x[0], reverse=True)
    selected = scored[:limit]

    results: List[ProductResponse] = []
    for score, prod, reasons in selected:
        results.append(ProductResponse(
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
            relevance_score=round(score, 1)
        ))

    return results

def get_related_products(db: Session, product_id: int, limit: int = 4) -> List[ProductResponse]:
    """
    Returns related in-stock products in the same category or brand, excluding the current product.
    """
    target = db.query(Product).filter(Product.id == product_id).first()
    if not target:
        return []

    candidates = (
        db.query(Product)
        .filter(
            Product.id != product_id,
            Product.category == target.category,
            Product.stock_quantity > 0
        )
        .order_by(Product.rating.desc())
        .limit(limit)
        .all()
    )

    # If category has fewer products, fill with high-rated products in other categories
    if len(candidates) < limit:
        fill_count = limit - len(candidates)
        existing_ids = [c.id for c in candidates] + [product_id]
        extras = (
            db.query(Product)
            .filter(~Product.id.in_(existing_ids), Product.stock_quantity > 0)
            .order_by(Product.rating.desc())
            .limit(fill_count)
            .all()
        )
        candidates.extend(extras)

    results: List[ProductResponse] = []
    for c in candidates:
        results.append(ProductResponse(
            id=c.id,
            name=c.name,
            category=c.category,
            brand=c.brand,
            price=c.price,
            stock_quantity=c.stock_quantity,
            description=c.description,
            rating=c.rating,
            tags=c.tags,
            image_url=c.image_url,
            specs=c.specs,
            created_at=c.created_at,
            why_recommended=[
                f"Similar to {target.name[:25]}...",
                f"Top choice in {c.category}",
                f"In stock ({c.stock_quantity} left)"
            ],
            relevance_score=80.0
        ))
    return results
