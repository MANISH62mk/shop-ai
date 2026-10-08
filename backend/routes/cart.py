from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import CartItem, Product
from backend.schemas import (
    CartItemCreate,
    CartItemUpdate,
    CartItemResponse,
    CartSummaryResponse,
    ProductResponse
)

router = APIRouter(prefix="/api/cart", tags=["Cart"])

@router.get("", response_model=CartSummaryResponse)
def get_cart(session_id: str = Query(...), db: Session = Depends(get_db)):
    """
    Retrieves user cart items, computes subtotal and total,
    and validates live stock availability for each item.
    """
    items = db.query(CartItem).filter(CartItem.session_id == session_id).all()

    item_responses: List[CartItemResponse] = []
    subtotal = 0.0

    for item in items:
        product = item.product
        if not product:
            continue

        item_subtotal = product.price * item.quantity
        subtotal += item_subtotal

        is_stock_available = product.stock_quantity >= item.quantity
        available_stock = product.stock_quantity

        prod_resp = ProductResponse(
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
            why_recommended=[
                "In Stock" if product.stock_quantity > 0 else "Out of Stock"
            ]
        )

        item_responses.append(CartItemResponse(
            id=item.id,
            session_id=item.session_id,
            product_id=item.product_id,
            quantity=item.quantity,
            product=prod_resp,
            subtotal=item_subtotal,
            is_stock_available=is_stock_available,
            available_stock=available_stock
        ))

    total = subtotal # Free demo shipping, tax inclusive
    item_count = sum(item.quantity for item in items)

    return CartSummaryResponse(
        items=item_responses,
        subtotal=round(subtotal, 2),
        tax=0.0,
        shipping=0.0,
        total=round(total, 2),
        item_count=item_count
    )

@router.post("", response_model=CartSummaryResponse)
def add_to_cart(payload: CartItemCreate, db: Session = Depends(get_db)):
    """
    Adds a product to the cart or increments its quantity.
    Strictly verifies live inventory and prevents exceeding stock.
    """
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock_quantity <= 0:
        raise HTTPException(status_code=400, detail="This product is currently out of stock.")

    # Check existing item
    cart_item = db.query(CartItem).filter(
        CartItem.session_id == payload.session_id,
        CartItem.product_id == payload.product_id
    ).first()

    target_qty = payload.quantity
    if cart_item:
        target_qty = cart_item.quantity + payload.quantity

    if target_qty > product.stock_quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot add {payload.quantity} more. Only {product.stock_quantity} available in stock."
        )

    if cart_item:
        cart_item.quantity = target_qty
    else:
        cart_item = CartItem(
            session_id=payload.session_id,
            product_id=payload.product_id,
            quantity=payload.quantity
        )
        db.add(cart_item)

    db.commit()
    return get_cart(session_id=payload.session_id, db=db)

@router.put("/{cart_item_id}", response_model=CartSummaryResponse)
def update_cart_quantity(cart_item_id: int, payload: CartItemUpdate, db: Session = Depends(get_db)):
    """
    Updates the quantity of a specific cart item, enforcing stock limits.
    """
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    product = cart_item.product
    if payload.quantity > product.stock_quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Requested quantity {payload.quantity} exceeds available stock ({product.stock_quantity})."
        )

    if payload.quantity <= 0:
        session_id = cart_item.session_id
        db.delete(cart_item)
        db.commit()
        return get_cart(session_id=session_id, db=db)

    cart_item.quantity = payload.quantity
    db.commit()

    return get_cart(session_id=cart_item.session_id, db=db)

@router.delete("/{cart_item_id}", response_model=CartSummaryResponse)
def remove_from_cart(cart_item_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    session_id = cart_item.session_id
    db.delete(cart_item)
    db.commit()

    return get_cart(session_id=session_id, db=db)

@router.delete("", response_model=CartSummaryResponse)
def clear_cart(session_id: str = Query(...), db: Session = Depends(get_db)):
    db.query(CartItem).filter(CartItem.session_id == session_id).delete()
    db.commit()
    return get_cart(session_id=session_id, db=db)
