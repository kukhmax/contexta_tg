from sqlalchemy.orm import Session
from app.models.user import User, SubscriptionTier
from app.schemas.user import UserCreate
from typing import Optional
from datetime import datetime, timedelta

def set_user_premium(db: Session, telegram_id: int, days: int = 30) -> User:
    """
    Выдает пользователю премиум подписку.
    """
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        return None
        
    user.tier = SubscriptionTier.PREMIUM
    
    # Если подписка уже есть, продлеваем
    if user.subscription_expires_at and user.subscription_expires_at > datetime.utcnow():
        user.subscription_expires_at += timedelta(days=days)
    else:
        user.subscription_expires_at = datetime.utcnow() + timedelta(days=days)
        
    db.commit()
    db.refresh(user)
    return user

def get_user_by_telegram_id(db: Session, telegram_id: int) -> Optional[User]:
    """
    Получает пользователя по Telegram ID.
    """
    return db.query(User).filter(User.telegram_id == telegram_id).first()

def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Создает нового пользователя в базе данных.
    """
    db_user = User(
        telegram_id=user_in.telegram_id,
        username=user_in.username,
        first_name=user_in.first_name,
        language_code=user_in.language_code
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
