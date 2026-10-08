from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    email: str
    name: str
    role: str = "customer"

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str
    category: str
    brand: str
    price: float
    stock_quantity: int = 0
    description: str
    rating: float = 4.0
    tags: str = ""
    image_url: str
    specs: Optional[str] = "{}"

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    tags: Optional[str] = None
    image_url: Optional[str] = None
    specs: Optional[str] = None

class ProductStockUpdate(BaseModel):
    stock_quantity: int = Field(ge=0)

class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime.datetime] = None
    why_recommended: Optional[List[str]] = None
    relevance_score: Optional[float] = None

    class Config:
        from_attributes = True

# --- Cart Schemas ---
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)
    session_id: str

class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1)

class CartItemResponse(BaseModel):
    id: int
    session_id: str
    product_id: int
    quantity: int
    product: ProductResponse
    subtotal: float
    is_stock_available: bool
    available_stock: int

    class Config:
        from_attributes = True

class CartSummaryResponse(BaseModel):
    items: List[CartItemResponse]
    subtotal: float
    tax: float
    shipping: float
    total: float
    item_count: int

# --- Order Schemas ---
class CheckoutRequest(BaseModel):
    session_id: str
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str
    payment_method: str = "Cash on Delivery" # or "Demo Card Payment"

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    unit_price: float
    quantity: int
    subtotal: float

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str
    payment_method: str
    total_amount: float
    status: str
    created_at: Optional[datetime.datetime] = None
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True

# --- AI & Semantic Search Schemas ---
class AISearchRequest(BaseModel):
    query: str
    session_id: Optional[str] = "guest-default"

class ExtractedIntent(BaseModel):
    category: Optional[str] = None
    max_budget: Optional[float] = None
    min_budget: Optional[float] = None
    brand: Optional[str] = None
    use_case: Optional[str] = None
    keywords: List[str] = []
    features_requested: List[str] = []

class AISearchResponse(BaseModel):
    query: str
    extracted_intent: ExtractedIntent
    response_message: str
    products: List[ProductResponse]
    out_of_stock_alert: Optional[str] = None
    total_found: int

# --- Admin Schemas ---
class AdminDashboardStats(BaseModel):
    total_products: int
    total_orders: int
    total_revenue: float
    products_sold: int
    low_stock_products: int

class TopSellingProduct(BaseModel):
    product_id: int
    product_name: str
    category: str
    units_sold: int
    revenue_generated: float

class DailySalesData(BaseModel):
    date: str
    revenue: float
    orders_count: int

class AdminAnalyticsResponse(BaseModel):
    stats: AdminDashboardStats
    sales_over_time: List[DailySalesData]
    top_selling: List[TopSellingProduct]

class CSVImportResult(BaseModel):
    success: bool
    imported_count: int
    failed_count: int
    errors: List[str]
    sample_preview: List[Dict[str, Any]]
