from groq import Groq
from app.core.config import settings
import json
import logging

logger = logging.getLogger(__name__)

async def generate_story_with_ai(word: str, level: str, target_lang: str, native_lang: str) -> dict:
    """
    Генерирует историю через Groq API.
    Возвращает словарь с текстом истории и списком выделенных слов.
    """
    if not settings.GROQ_API_KEY:
        raise ValueError("API Key for Groq is not configured / Ключ Groq API не настроен")

    client = Groq(api_key=settings.GROQ_API_KEY)
    
    # Промпт для генерации
    prompt = f"""
    You are a professional language teacher.
    Create a short, engaging story ({level} level) in {target_lang} that naturally uses the word/phrase "{word}".
    IMPORTANT: You MUST use the word "{word}" at least 3 times in the story, utilizing DIFFERENT grammatical forms (conjugations, pluralizations, cases, etc.) where possible.
    The story should be 100-150 words long.
    
    Output format must be strictly JSON with keys:
    - "content": the story text in {target_lang}
    - "highlighted_words": a list of strings containing ONLY the different forms of the word "{word}" used in the text. Do NOT include any other vocabulary words.

    Do not include any other text, only the JSON.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that outputs only JSON."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="meta-llama/llama-guard-4-12b", # Mixtral deprecated, using Llama 3.3
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        
        response_content = chat_completion.choices[0].message.content
        return json.loads(response_content)
        
    except Exception as e:
        logger.error(f"Error generating story: {e}")
        raise e
