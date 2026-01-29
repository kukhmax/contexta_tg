import hmac
import hashlib
import json
from urllib.parse import parse_qsl
from app.core.config import settings
from typing import Dict, Any, Optional

def validate_telegram_data(init_data: str, bot_token: str) -> Optional[Dict[str, Any]]:
    """
    Validates the initData received from Telegram Web App.
    Returns the parsed data if valid, None otherwise.
    """
    if not bot_token:
        # For development without token validation (NOT RECOMMENDED for prod)
        # return parse_init_data(init_data) 
        pass

    try:
        parsed_data = dict(parse_qsl(init_data))
    except ValueError:
        return None

    if "hash" not in parsed_data:
        return None

    received_hash = parsed_data.pop("hash")
    
    # Sort keys alphabetically
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items())
    )
    
    # Calculate secret key
    secret_key = hmac.new(
        key=b"WebAppData",
        msg=bot_token.encode(),
        digestmod=hashlib.sha256
    ).digest()
    
    # Calculate hash
    calculated_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
    
    if calculated_hash != received_hash:
        return None
        
    # JSON parse user object if present
    if "user" in parsed_data:
        try:
            parsed_data["user"] = json.loads(parsed_data["user"])
        except json.JSONDecodeError:
            pass
            
    return parsed_data
