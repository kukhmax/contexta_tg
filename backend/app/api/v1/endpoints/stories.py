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
    2. Проверяет лимиты (5 запросов в день)
    3. Отправляет запрос в LLM (Groq)
    4. Сохраняет историю в БД
    5. Возвращает результат
    """
    # 1. Поиск пользователя
    user = db.query(User).filter(User.telegram_id == request.telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    from app.models.user import SubscriptionTier
    from app.core.rate_limit import check_rate_limit
    
    # Проверка лимитов (5 историй в день для Free, безлимит для Premium)
    if user.tier != SubscriptionTier.PREMIUM:
        # Для Free тарифа
        await check_rate_limit(request.telegram_id, limit=5)

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
        translation=ai_result.get("translation", ""),
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

@router.delete("/{story_id}")
def delete_story(
    story_id: int,
    telegram_id: int,
    db: Session = Depends(get_db)
):
    """Удалить историю"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
        
    story = db.query(Story).filter(Story.id == story_id, Story.user_id == user.id).first()
    if not story:
        raise HTTPException(status_code=404, detail="История не найдена")
        
    db.delete(story)
    db.commit()
    return {"ok": True}
