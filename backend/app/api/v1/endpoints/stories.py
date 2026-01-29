from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services import ai_service
from app.schemas.story import StoryGenerateRequest, StoryResponse
from app.models.story import Story
from app.models.user import User
from app.core.config import settings

router = APIRouter()

# TODO: В продакшене нужно получать user_id из токена или initData
# Для MVP передаем user_id в хедере или параметре (упрощение для теста)
# Или просто принимаем telegram_id в body, но это небезопасно. 
# Лучший вариант для MVP без JWT - передавать initData в хедере Authorization и валидировать её в middleware, 
# извлекая user_id.
# Пока сделаем упрощенную версию: требуем telegram_id в запросе для привязки.

class GenerateRequestWithAuth(StoryGenerateRequest):
    telegram_id: int

@router.post("/generate", response_model=StoryResponse)
async def generate_story(
    request: GenerateRequestWithAuth,
    db: Session = Depends(get_db)
):
    """
    Генерация истории с помощью AI.
    
    1. Ищет пользователя по telegram_id
    2. Отправляет запрос в LLM (Groq)
    3. Сохраняет историю в БД
    4. Возвращает результат
    """
    # 1. Поиск пользователя
    user = db.query(User).filter(User.telegram_id == request.telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # 2. Генерация
    try:
        ai_result = await ai_service.generate_story_with_ai(
            word=request.word,
            level=request.level,
            target_lang=request.target_language,
            native_lang=request.native_language
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации: {str(e)}")

    # 3. Сохранение
    db_story = Story(
        user_id=user.id,
        input_word=request.word,
        language_level=request.level,
        target_language=request.target_language,
        content=ai_result.get("content", ""),
        highlighted_words=ai_result.get("highlighted_words", [])
    )
    db.add(db_story)
    db.commit()
    db.refresh(db_story)

    return db_story

@router.get("/", response_model=list[StoryResponse])
def get_my_stories(
    telegram_id: int,
    db: Session = Depends(get_db)
):
    """Получить список историй пользователя"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
         raise HTTPException(status_code=404, detail="Пользователь не найден")
         
    return db.query(Story).filter(Story.user_id == user.id).order_by(Story.created_at.desc()).all()
