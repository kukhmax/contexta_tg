from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StoryGenerateRequest(BaseModel):
    """Схема запроса на генерацию истории"""
    word: str
    level: str  # A1, A2, B1, etc.
    target_language: str
    native_language: str = "ru"

class StoryResponse(BaseModel):
    """Схема ответа с историей"""
    id: int
    content: str
    translation: Optional[str] = None
    highlighted_words: List[str]
    input_word: str
    created_at: datetime
    
    class Config:
        from_attributes = True
