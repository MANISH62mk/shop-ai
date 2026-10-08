from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User
from backend.schemas import UserLogin, UserResponse

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=UserResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Demo authentication endpoint verifying customer or admin credentials.
    Demo Customer: demo@shopai.com / demo123
    Admin: admin@shopai.com / admin123
    """
    user = db.query(User).filter(User.email == payload.email.strip().lower()).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email address.")

    if user.password_hash != payload.password.strip():
        raise HTTPException(status_code=401, detail="Invalid password.")

    return user

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    """
    Returns list of users for easy demo selection in UI.
    """
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "name": u.name,
            "role": u.role
        } for u in users
    ]
