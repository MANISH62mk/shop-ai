from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_db
from backend.routes import (
    ai,
    products,
    cart,
    orders,
    admin,
    auth
)

app = FastAPI(
    title="SHOPAI — AI-Powered E-Commerce Assistant API",
    description="Backend API for ShopAI with natural-language semantic search, live inventory management, and demo checkout.",
    version="1.0.0"
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development allow all or localhost:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event to ensure SQLite tables and seeds are present
@app.on_event("startup")
def on_startup():
    init_db()

# Include Routers
app.include_router(ai.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(admin.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "ShopAI Backend API",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "shopai-backend"}
