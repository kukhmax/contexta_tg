from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import enum

class Base(DeclarativeBase):
    pass

class UserRole(enum.Enum):
    USER = "user"       # Обычный пользователь
    ADMIN = "admin"     # Администратор

class SubscriptionTier(enum.Enum):
    FREE = "free"       # Бесплатный тариф
    PREMIUM = "premium" # Премиум тариф
    PRO = "pro"         # Профессиональный тариф

class User(Base):
    """
    Модель пользователя Telegram.
    Хранит информацию о профиле, настройках языка и статусе подписки.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False) # ID пользователя в Telegram
    username = Column(String, nullable=True)     # Никнейм (@username)
    first_name = Column(String, nullable=True)   # Имя
    language_code = Column(String, nullable=True) # Язык интерфейса пользователя
    
    # Настройки обучения
    native_language = Column(String, default="ru")  # Родной язык
    learning_language = Column(String, default="en") # Изучаемый язык
    
    # Подписка
    tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE) # Уровень подписки
    subscription_expires_at = Column(DateTime, nullable=True) # Дата истечения подписки
    
    # Статистика и роль
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.utcnow) # Дата регистрации
    
    def __repr__(self):
        return f"<User {self.telegram_id}>"
