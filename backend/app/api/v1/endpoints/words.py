from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.api.deps import get_db
from app.services import word_service
from app.models.user import User

router = APIRouter()

# Schemas
class WordBase(BaseModel):
    word: str
    translation: Optional[str] = None
    context: Optional[str] = None

class WordCreate(WordBase):
    telegram_id: int # Для MVP

class WordInDB(WordBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[WordInDB])
def read_words(
    telegram_id: int,
    db: Session = Depends(get_db)
):
    """
    Получает список слов пользователя.
    """
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return word_service.get_words_by_user(db, user.id)

@router.post("/", response_model=WordInDB)
def create_word(
    word_in: WordCreate,
    db: Session = Depends(get_db)
):
    """
    Сохраняет слово.
    """
    user = db.query(User).filter(User.telegram_id == word_in.telegram_id).first()
    if not user:
         raise HTTPException(status_code=404, detail="User not found")
         
    return word_service.create_word(
        db=db,
        word=word_in.word,
        user_id=user.id,
        translation=word_in.translation,
        context=word_in.context
    )

@router.delete("/{word_id}")
def delete_word(
    word_id: int,
    telegram_id: int,
    db: Session = Depends(get_db)
):
    """
    Удаляет слово.
    """
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    success = word_service.delete_word(db, word_id, user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Word not found")
        
    return {"ok": True}
