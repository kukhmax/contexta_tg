from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.security import validate_telegram_data
from app.core.config import settings
from app.services import user_service
from app.schemas.user import User, UserCreate
from pydantic import BaseModel

router = APIRouter()

class TelegramAuth(BaseModel):
    initData: str

@router.post("/login", response_model=User)
def login_telegram(
    auth_data: TelegramAuth,
    db: Session = Depends(get_db)
):
    """
    Authenticate user via Telegram Web App initData.
    Creates user if not exists.
    """
    if not settings.BOT_TOKEN:
        raise HTTPException(status_code=500, detail="Bot token not configured")

    # Validate initData
    user_data = validate_telegram_data(auth_data.initData, settings.BOT_TOKEN)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid authentication data")
    
    tg_user = user_data.get("user")
    if not tg_user:
        raise HTTPException(status_code=400, detail="User data missing in initData")

    # Check if user exists
    user = user_service.get_user_by_telegram_id(db, tg_user["id"])
    if not user:
        # Create new user
        user_in = UserCreate(
            telegram_id=tg_user["id"],
            username=tg_user.get("username"),
            first_name=tg_user.get("first_name"),
            language_code=tg_user.get("language_code")
        )
        user = user_service.create_user(db, user_in)
    
    return user
