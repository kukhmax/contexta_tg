from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from typing import Optional

def get_user_by_telegram_id(db: Session, telegram_id: int) -> Optional[User]:
    return db.query(User).filter(User.telegram_id == telegram_id).first()

def create_user(db: Session, user_in: UserCreate) -> User:
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
