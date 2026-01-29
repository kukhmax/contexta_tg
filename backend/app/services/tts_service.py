import edge_tts
import os
import uuid
from app.core.config import settings

VOICES = {
    "en": "en-US-ChristopherNeural",
    "ru": "ru-RU-DmitryNeural", 
    "pt": "pt-PT-RaquelNeural",
    "es": "es-ES-AlvaroNeural",
    "pl": "pl-PL-MarekNeural"
}

AUDIO_DIR = "/tmp/audio_cache" # В Docker это будет внутри контейнера

if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

async def generate_audio_file(text: str, language: str) -> str:
    """
    Генерирует аудио файл из текста.
    Возвращает путь к временному файлу.
    TODO: В продакшене лучше стримить поток или сохранять в S3.
    """
    voice = VOICES.get(language, "en-US-ChristopherNeural")
    communicate = edge_tts.Communicate(text, voice)
    
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)
    
    await communicate.save(filepath)
    return filepath

async def cleanup_audio_file(filepath: str):
    """Удаляет временный файл"""
    if os.path.exists(filepath):
        os.remove(filepath)
