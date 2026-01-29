from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services import user_service
from app.schemas.user import User

router = APIRouter()

@router.get("/me", response_model=User)
def read_users_me(
    telegram_id: int,
    db: Session = Depends(get_db)
):
    """
    Get current user by telegram_id. 
    TODO: Add proper JWT or Session auth later, for now relying on telegram_id passed ensuring it matches validated session context in a real app.
    For this MVP, we might trust the client side IF we validate initData on every request OR issue a JWT on login.
    For simplicity in MVP Step 3, we will just return user by ID, assuming /login was called first.
    """
    user = user_service.get_user_by_telegram_id(db, telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
