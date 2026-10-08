from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Product
from backend.schemas import AISearchRequest, AISearchResponse, ProductResponse
from backend.services.ai_search import perform_ai_semantic_search
from backend.services.recommendations import get_recommendations_for_user

router = APIRouter(prefix="/api/ai", tags=["AI Shopping Assistant"])

@router.post("/search", response_model=AISearchResponse)
def search_ai(request: AISearchRequest, db: Session = Depends(get_db)):
    """
    Main Natural Language Shopping Assistant endpoint:
    Processes natural queries like 'I need a lightweight laptop for coding under ₹60,000'
    Extracts intent, performs semantic scoring, checks stock, and explains recommendations.
    """
    return perform_ai_semantic_search(db, request.query)

@router.get("/recommendations", response_model=List[ProductResponse])
def get_recommendations(
    viewed_ids: Optional[str] = Query(None, description="Comma-separated IDs of viewed products"),
    category: Optional[str] = None,
    user_id: Optional[int] = None,
    limit: int = 6,
    db: Session = Depends(get_db)
):
    """
    Returns AI-personalized product recommendations based on browsing context and rating.
    Only recommends products with live stock_quantity > 0.
    """
    parsed_ids = []
    if viewed_ids:
        try:
            parsed_ids = [int(x.strip()) for x in viewed_ids.split(",") if x.strip().isdigit()]
        except Exception:
            parsed_ids = []

    return get_recommendations_for_user(
        db=db,
        viewed_product_ids=parsed_ids,
        preferred_category=category,
        user_id=user_id,
        limit=limit
    )

@router.get("/popular-queries")
def get_popular_queries():
    """
    Curated realistic prompts for immediate 1-click test exploration.
    """
    return [
        {
            "query": "I need a lightweight laptop for coding under ₹60,000",
            "tag": "Coding Laptops",
            "icon": "Laptop"
        },
        {
            "query": "Show me wireless headphones under 3000",
            "tag": "Audio & Bass",
            "icon": "Headphones"
        },
        {
            "query": "I need a phone with good camera under 25000",
            "tag": "Camera Phones",
            "icon": "Smartphone"
        },
        {
            "query": "Suggest something for gaming",
            "tag": "Gaming Setup",
            "icon": "Gamepad2"
        },
        {
            "query": "Find a monitor for coding",
            "tag": "Productivity Display",
            "icon": "Monitor"
        },
        {
            "query": "Tactile mechanical keyboard for typing",
            "tag": "Keyboards",
            "icon": "Keyboard"
        }
    ]
