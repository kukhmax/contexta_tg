from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .user import Base

class Story(Base):
    """
    Модель сгенерированной истории.
    Хранит текст истории, параметры генерации и ссылку на пользователя.
    """
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id")) # Внешний ключ на пользователя
    
    input_word = Column(String, nullable=False)       # Введенное слово/фраза
    language_level = Column(String, nullable=False)   # Уровень (A1, A2, etc.)
    target_language = Column(String, nullable=False)  # Изучаемый язык
    
    content = Column(Text, nullable=False)            # Текст истории
    highlighted_words = Column(JSON, nullable=True)   # Список слов для подсветки (JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow) # Дата создания
    
    # Связи (Relationships)
    user = relationship("User", backref="stories")
    
    def __repr__(self):
        return f"<Story {self.id} by {self.user_id}>"
