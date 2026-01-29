from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Базовая схема пользователя"""
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    language_code: Optional[str] = None

class UserCreate(UserBase):
    """Схема для создания пользователя"""
    pass

class UserUpdate(UserBase):
    """Схема для обновления пользователя"""
    pass

class UserInDBBase(UserBase):
    """Базовая схема пользователя в БД"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class User(UserInDBBase):
    """Публичная схема пользователя"""
    pass
