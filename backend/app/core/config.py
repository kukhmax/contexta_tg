from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Конфигурация приложения.
    Считывает переменные окружения из .env файла.
    """
    PROJECT_NAME: str = "Contexta"
    API_V1_STR: str = "/api/v1"
    
    # Подключение к базе данных и Redis
    DATABASE_URL: str
    REDIS_URL: str = "redis://redis:6379/0"
    
    # Токены и ключи API
    BOT_TOKEN: Optional[str] = None     # Токен Telegram бота
    GROQ_API_KEY: Optional[str] = None  # Ключ API для AI генерации
    
    # Gemini Configuration
    IS_GEMINI: bool = False             # Флаг использования Gemini вместо Groq
    GEMINI_API_KEY: Optional[str] = None # Ключ API для Google Gemini
    
    class Config:
        env_file = ".env"

settings = Settings()
