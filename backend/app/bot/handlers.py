from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.bot.keyboards import get_main_keyboard

router = Router()

# URL вашего Web App (в продакшене это будет HTTPS ссылка)
# Пока используем localhost или туннель, но для кнопки нужна полная ссылка.
# В реальной жизни это берется из конфига.
WEBAPP_URL = "https://t.me/ContextaBot/app" # Заглушка, нужно заменить на реальную

@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Обработчик команды /start.
    Приветствует пользователя и предлагает запустить Mini App.
    """
    await message.answer(
        "👋 Привет! Я Contexta Bot.\n\n"
        "Я помогу тебе изучать языки через интересные истории.\n"
        "Нажми кнопку ниже, чтобы начать! 👇",
        reply_markup=get_main_keyboard(WEBAPP_URL)
    )
