from sqlalchemy.orm import Session
from app.models.word import SavedWord
from typing import List, Optional

def get_words_by_user(db: Session, user_id: int) -> List[SavedWord]:
    """Получает все сохраненные слова пользователя"""
    return db.query(SavedWord).filter(SavedWord.user_id == user_id).order_by(SavedWord.created_at.desc()).all()

def create_word(db: Session, word: str, user_id: int, translation: Optional[str] = None, context: Optional[str] = None) -> SavedWord:
    """Сохраняет новое слово"""
    db_word = SavedWord(
        word=word,
        user_id=user_id,
        translation=translation,
        context=context
    )
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word

def delete_word(db: Session, word_id: int, user_id: int) -> bool:
    """Удаляет слово"""
    db_word = db.query(SavedWord).filter(SavedWord.id == word_id, SavedWord.user_id == user_id).first()
    if db_word:
        db.delete(db_word)
        db.commit()
        return True
    return False
