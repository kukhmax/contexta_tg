from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_keyboard(webapp_url: str) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру главного меню с кнопкой запуска Web App.
    
    :param webapp_url: URL адрес Mini App
    :return: Объект InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🚀 Запустить приложение",
        web_app=WebAppInfo(url=webapp_url)
    )
    return builder.as_markup()
