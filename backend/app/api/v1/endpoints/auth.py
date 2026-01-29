from fastapi import APIRouter, Depends, HTTPException
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
    Аутентификация пользователя через initData от Telegram Web App.
    Если пользователь не существует, он будет создан автоматически.
    
    - **initData**: Строка инициализации, полученная от Telegram Mini App
    """
    if not settings.BOT_TOKEN:
        raise HTTPException(status_code=500, detail="Токен бота не настроен (BOT_TOKEN)")

    # Валидация initData
    user_data = validate_telegram_data(auth_data.initData, settings.BOT_TOKEN)
    if not user_data:
        raise HTTPException(status_code=401, detail="Неверные данные аутентификации (Invalid auth data)")
    
    tg_user = user_data.get("user")
    if not tg_user:
        raise HTTPException(status_code=400, detail="В initData отсутствуют данные пользователя")

    # Проверяем, существует ли пользователь
    user = user_service.get_user_by_telegram_id(db, tg_user["id"])
    if not user:
        # Создаем нового пользователя
        user_in = UserCreate(
            telegram_id=tg_user["id"],
            username=tg_user.get("username"),
            first_name=tg_user.get("first_name"),
            language_code=tg_user.get("language_code")
        )
        user = user_service.create_user(db, user_in)
    
    return user
