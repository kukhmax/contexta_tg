from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Contexta"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str
    REDIS_URL: str = "redis://redis:6379/0"
    
    BOT_TOKEN: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
