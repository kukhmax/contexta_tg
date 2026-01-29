from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router

# Создание экземпляра FastAPI приложения
app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Настройка CORS (Cross-Origin Resource Sharing)
# Разрешаем запросы с любых источников (в продакшене лучше ограничить)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """Простой эндпоинт для проверки работоспособности API"""
    return {"message": "Contexta API is running / API запущен"}
