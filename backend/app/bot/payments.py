from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.filters import Command
from app.api.deps_bot import get_db_session
from app.services import user_service
from app.core.config import settings
import logging

router = Router()
logger = logging.getLogger(__name__)

# Цены (1 XTR = 1 Star)
PRICES = [
    LabeledPrice(label="Premium 1 Month", amount=50), # 50 Stars
]

@router.message(Command("buy"))
async def cmd_buy(message: Message):
    """
    Команда /buy для покупки премиума.
    """
    await message.answer_invoice(
        title="Contexta Premium",
        description="Unlock full access: Unlimited stories, audio, and vocabulary.",
        payload="premium_1_month",
        provider_token="", # Для Telegram Stars токен должен быть пустым!
        currency="XTR",
        prices=PRICES,
        start_parameter="premium-sub",
    )

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    """
    Подтверждение готовности принять оплату.
    """
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    """
    Обработка успешной оплаты.
    """
    payment = message.successful_payment
    telegram_id = message.from_user.id
    
    logger.info(f"Payment received from {telegram_id}: {payment}")
    
    # Выдача премиума
    # Так как мы в aiogram, нам нужно получить сессию БД вручную.
    # Используем наш генератор и context manager
    
    try:
        db = next(get_db_session()) # Получаем сессию
        user = user_service.set_user_premium(db, telegram_id, days=30)
        
        await message.answer(
            f"🎉 Payment successful! Premium activated until {user.subscription_expires_at.date()}.\n"
            "Enjoy unlimited learning!"
        )
    except Exception as e:
        logger.error(f"Failed to upgrade user {telegram_id}: {e}")
        await message.answer("⚠️ Payment accepted, but failed to activate Premium. Support contacted.")
