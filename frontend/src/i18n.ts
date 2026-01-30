import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Ресурсы переводов
const resources = {
    en: {
        translation: {
            "welcome": "Welcome to Contexta",
            "start_learning": "Start Learning",
            "history": "History",
            "profile": "Profile",
            "word_input_placeholder": "Enter a word or phrase...",
            "generate_btn": "Generate Story",
            "select_level": "Select Level",
            "select_language": "Select Language",
            "loading": "Loading...",
            "error": "Something went wrong",
            "show_translation": "Show Translation",
            "hide_translation": "Hide Translation",
            "listen": "Listen",
            "my_vocabulary": "My Vocabulary"
        }
    },
    ru: {
        translation: {
            "welcome": "Добро пожаловать в Contexta",
            "start_learning": "Начать обучение",
            "history": "История",
            "profile": "Профиль",
            "word_input_placeholder": "Введите слово или фразу...",
            "generate_btn": "Создать историю",
            "select_level": "Выберите уровень",
            "select_language": "Выберите язык",
            "loading": "Загрузка...",
            "error": "Что-то пошло не так",
            "show_translation": "Показать перевод",
            "hide_translation": "Скрыть перевод",
            "listen": "Слушать",
            "my_vocabulary": "Мой Словарь"
        }
    }
};

i18n
    .use(initReactI18next)
    .init({
        resources,
        lng: "ru", // Язык по умолчанию для MVP - Русский
        fallbackLng: "en",
        interpolation: {
            escapeValue: false // React уже защищает от XSS
        }
    });

export default i18n;
