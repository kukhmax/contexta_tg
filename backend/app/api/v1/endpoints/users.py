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
    Получение профиля текущего пользователя по telegram_id.
    
    TODO: В будущем добавить JWT авторизацию или сессии. 
    Пока для MVP мы доверяем клиенту, предполагая, что /auth/login прошел успешно.
    """
    user = user_service.get_user_by_telegram_id(db, telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
