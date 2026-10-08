from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Order, OrderItem, CartItem, Product, User
from backend.schemas import CheckoutRequest, OrderResponse, OrderItemResponse

router = APIRouter(prefix="/api/orders", tags=["Orders & Checkout"])

@router.post("/checkout", response_model=OrderResponse)
def checkout_cart(payload: CheckoutRequest, db: Session = Depends(get_db)):
    """
    Executes atomic checkout:
    1. Validates cart items and verifies stock availability.
    2. Decrements product stock automatically.
    3. Creates Order and OrderItem records.
    4. Clears user's cart session.
    5. Returns confirmed order details.
    """
    cart_items = db.query(CartItem).filter(CartItem.session_id == payload.session_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty. Please add items before checking out.")

    # 1. Validate all stock availability before committing changes
    order_line_items = []
    total_amount = 0.0

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).with_for_update().first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} no longer exists.")

        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for '{product.name}'. Available: {product.stock_quantity}, in cart: {item.quantity}."
            )

        line_subtotal = round(product.price * item.quantity, 2)
        total_amount += line_subtotal
        order_line_items.append((product, item.quantity, line_subtotal))

    # Match user if email matches
    user = db.query(User).filter(User.email == payload.customer_email.lower().strip()).first()

    # 2. Create the Order
    new_order = Order(
        user_id=user.id if user else None,
        customer_name=payload.customer_name.strip(),
        customer_email=payload.customer_email.strip(),
        customer_phone=payload.customer_phone.strip(),
        shipping_address=payload.shipping_address.strip(),
        payment_method=payload.payment_method,
        total_amount=round(total_amount, 2),
        status="Confirmed"
    )
    db.add(new_order)
    db.flush() # Assigns new_order.id

    # 3. Create OrderItems & Decrease stock
    for product, quantity, line_subtotal in order_line_items:
        # Decrease stock automatically
        product.stock_quantity = product.stock_quantity - quantity

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            product_name=product.name,
            unit_price=product.price,
            quantity=quantity,
            subtotal=line_subtotal
        )
        db.add(order_item)

    # 4. Clear the cart session
    db.query(CartItem).filter(CartItem.session_id == payload.session_id).delete()

    db.commit()
    db.refresh(new_order)

    # Build response
    item_responses = [
        OrderItemResponse(
            id=item.id,
            product_id=item.product_id,
            product_name=item.product_name,
            unit_price=item.unit_price,
            quantity=item.quantity,
            subtotal=item.subtotal
        ) for item in new_order.items
    ]

    return OrderResponse(
        id=new_order.id,
        user_id=new_order.user_id,
        customer_name=new_order.customer_name,
        customer_email=new_order.customer_email,
        customer_phone=new_order.customer_phone,
        shipping_address=new_order.shipping_address,
        payment_method=new_order.payment_method,
        total_amount=new_order.total_amount,
        status=new_order.status,
        created_at=new_order.created_at,
        items=item_responses
    )

@router.get("", response_model=List[OrderResponse])
def get_orders(
    email: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Order).order_by(Order.created_at.desc())
    if email:
        query = query.filter(Order.customer_email.ilike(f"%{email.strip()}%"))

    orders = query.limit(limit).all()

    result = []
    for o in orders:
        items = [
            OrderItemResponse(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product_name,
                unit_price=item.unit_price,
                quantity=item.quantity,
                subtotal=item.subtotal
            ) for item in o.items
        ]
        result.append(OrderResponse(
            id=o.id,
            user_id=o.user_id,
            customer_name=o.customer_name,
            customer_email=o.customer_email,
            customer_phone=o.customer_phone,
            shipping_address=o.shipping_address,
            payment_method=o.payment_method,
            total_amount=o.total_amount,
            status=o.status,
            created_at=o.created_at,
            items=items
        ))
    return result

@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    items = [
        OrderItemResponse(
            id=item.id,
            product_id=item.product_id,
            product_name=item.product_name,
            unit_price=item.unit_price,
            quantity=item.quantity,
            subtotal=item.subtotal
        ) for item in order.items
    ]
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        customer_phone=order.customer_phone,
        shipping_address=order.shipping_address,
        payment_method=order.payment_method,
        total_amount=order.total_amount,
        status=order.status,
        created_at=order.created_at,
        items=items
    )
