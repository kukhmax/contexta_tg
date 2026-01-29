from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.story import Story
from app.models.user import User
from app.services import tts_service
import os

router = APIRouter()

@router.get("/{story_id}/audio")
async def get_story_audio(
    story_id: int,
    telegram_id: int, # Для проверки доступа
    db: Session = Depends(get_db)
):
    """
    Генерирует и возвращает аудио файл для истории.
    """
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
        
    # Проверка доступа (автор ли запрашивает?)
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user or story.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this story")

    try:
        # Генерация аудио
        # Используем язык истории или целевой язык? Логичнее читать на целевом языке.
        file_path = await tts_service.generate_audio_file(story.content, story.target_language)
        
        # Возвращаем файл и удаляем его после отправки (через BackgroundTask можно, 
        # но FileResponse с background=cleanup лучше)
        # Упрощенно для MVP: возвращаем файл, очистка будет отдельным процессом или 
        # надеемся на удаление системой. 
        # Правильный путь в FastAPI:
        from starlette.background import BackgroundTask
        
        return FileResponse(
            file_path, 
            media_type="audio/mpeg", 
            filename=f"story_{story_id}.mp3",
            background=BackgroundTask(tts_service.cleanup_audio_file, file_path)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
