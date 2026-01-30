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
    native_language: Optional[str] = "ru" # Язык пользователя для перевода

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
async def create_word(
    word_in: WordCreate,
    db: Session = Depends(get_db)
):
    """
    Сохраняет слово.
    """
    user = db.query(User).filter(User.telegram_id == word_in.telegram_id).first()
    if not user:
         raise HTTPException(status_code=404, detail="User not found")
         
    
    # Enrich word info via AI
    from app.services import ai_service
    
    # Значение по умолчанию если enrichment не сработает
    final_translation = word_in.translation
    final_context = word_in.context
    
    try:
        # Пытаемся получить перевод и спяжения через AI
        enrichment = await ai_service.enrich_word_info(
            word=word_in.word,
            context=word_in.context or "",
            native_lang=word_in.native_language or "ru"
        )
        
        if enrichment.get("translation"):
            final_translation = enrichment.get("translation")
            
        if enrichment.get("is_verb") and enrichment.get("conjugations"):
            # Если это глагол, заменяем контекст на спряжения
            final_context = f"Conjugations (Present): {enrichment.get('conjugations')}"
            
    except Exception as e:
        print(f"Enrichment failed: {e}")

    return word_service.create_word(
        db=db,
        word=word_in.word,
        user_id=user.id,
        translation=final_translation,
        context=final_context
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
