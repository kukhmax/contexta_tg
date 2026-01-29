from fastapi import HTTPException, Depends
from redis import Redis
from app.core.config import settings
from datetime import datetime

# Подключение к Redis
redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)

async def check_rate_limit(telegram_id: int, limit: int = 5, period_seconds: int = 86400):
    """
    Проверка лимита запросов для пользователя.
    
    :param telegram_id: ID пользователя
    :param limit: Максимальное количество запросов за период
    :param period_seconds: Период в секундах (по умолчанию сутки)
    """
    key = f"rate_limit:{telegram_id}:{datetime.utcnow().date()}"
    
    current_count = redis_client.get(key)
    
    if current_count and int(current_count) >= limit:
        raise HTTPException(
            status_code=429, 
            detail=f"Превышен лимит запросов. Доступно {limit} в день."
        )
    
    # Увеличиваем счетчик
    pipe = redis_client.pipeline()
    pipe.incr(key)
    if not current_count:
        pipe.expire(key, period_seconds)
    pipe.execute()

def get_redis_client():
    return redis_client
