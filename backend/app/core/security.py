import hmac
import hashlib
import json
from urllib.parse import parse_qsl
from typing import Dict, Any, Optional

def validate_telegram_data(init_data: str, bot_token: str) -> Optional[Dict[str, Any]]:
    """
    Проверяет валидность initData, полученных от Telegram Web App.
    Использует HMAC-SHA256 для проверки подписи.

    :param init_data: Строка запроса initData (raw query string)
    :param bot_token: Токен бота для проверки подписи
    :return: Словарь с данными, если проверка успешна, иначе None
    """
    if not bot_token:
        # В разработке можно пропустить проверку, если токен не задан, 
        # но в продакшене это критическая ошибка безопасности.
        return None

    try:
        # Парсим строку запроса в словарь
        parsed_data = dict(parse_qsl(init_data))
    except ValueError:
        return None

    if "hash" not in parsed_data:
        return None

    # Извлекаем полученный хеш
    received_hash = parsed_data.pop("hash")
    
    # Сортируем параметры по ключу в алфавитном порядке
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items())
    )
    
    # Вычисляем секретный ключ
    secret_key = hmac.new(
        key=b"WebAppData",
        msg=bot_token.encode(),
        digestmod=hashlib.sha256
    ).digest()
    
    # Вычисляем хеш от строки данных
    calculated_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
    
    # Сравниваем хеши
    if calculated_hash != received_hash:
        return None
        
    # Если есть поле 'user', парсим JSON внутри него
    if "user" in parsed_data:
        try:
            parsed_data["user"] = json.loads(parsed_data["user"])
        except json.JSONDecodeError:
            pass
            
    return parsed_data
