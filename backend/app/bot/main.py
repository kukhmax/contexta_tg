import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.core.config import settings
from app.bot.handlers import router as main_router
from app.bot.payments import router as payments_router

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """
    Главная функция запуска бота.
    """
    if not settings.BOT_TOKEN:
        logger.error("❌ BOT_TOKEN не найден в настройках!")
        return

    # Инициализация бота и диспетчера
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # Регистрация роутеров (обработчиков)
    dp.include_router(main_router)
    dp.include_router(payments_router)

    logger.info("🚀 Бот запущен и готов к работе...")
    
    # Удаляем вебхук и запускаем поллинг (для локальной разработки)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен.")
