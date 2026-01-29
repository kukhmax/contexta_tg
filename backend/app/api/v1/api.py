from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, stories, audio

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(stories.router, prefix="/stories", tags=["stories"])
api_router.include_router(audio.router, prefix="/stories", tags=["audio"]) # Монтируем как /stories/{id}/audio
