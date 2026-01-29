from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .user import Base

class SavedWord(Base):
    """
    Модель сохраненного слова для изучения.
    """
    __tablename__ = "saved_words"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    word = Column(String, nullable=False)        # Слово или фраза
    translation = Column(String, nullable=True)  # Перевод (опционально, можно заполнить позже AI)
    context = Column(Text, nullable=True)        # Контекст (предложение из истории)
    
    source = Column(String, default="story")     # Источник (story, manual, etc)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    user = relationship("User", backref="saved_words")
    
    def __repr__(self):
        return f"<SavedWord {self.word} by {self.user_id}>"
