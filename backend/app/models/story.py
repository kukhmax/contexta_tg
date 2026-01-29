from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .user import Base

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    input_word = Column(String, nullable=False)
    language_level = Column(String, nullable=False) # A1, A2, etc.
    target_language = Column(String, nullable=False)
    
    content = Column(Text, nullable=False)
    highlighted_words = Column(JSON, nullable=True) # List of words to highlight
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="stories")
    
    def __repr__(self):
        return f"<Story {self.id} by {self.user_id}>"
