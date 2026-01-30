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
        You are an experienced professional language teacher and curriculum designer.

        TASK:
        Create a short, coherent story in {target_lang} suitable strictly for CEFR level {level}.

        TARGET WORD / PHRASE:
        "{word}"

        GRAMMAR REQUIREMENTS (VERY IMPORTANT):
        - You MUST use the target word "{word}" in AT LEAST 3 DIFFERENT grammatical forms.
        - These forms must be meaningfully different, for example:
        - verb tense changes (present / past / future)
        - person conjugations (I / you / they)
        - singular vs plural
        - grammatical cases or genders (if applicable)
        - DO NOT repeat the same grammatical form twice.
        - Each form must be grammatically correct and natural.

        LEVEL CONTROL:
        - Use ONLY vocabulary, grammar, and sentence complexity appropriate for CEFR level {level}.
        - Avoid idioms, rare words, slang, or advanced constructions beyond this level.
        - Sentences should be short and clear for lower levels (A1–A2).

        STORY CONSTRAINTS:
        - Length: 100–120 words.
        - The story must feel natural and engaging, not like an exercise.
        - The target word forms must be naturally integrated into the story.

        HIGHLIGHTING RULES:
        - Wrap EVERY occurrence of the target word forms in the story with <b></b> HTML tags.
        - Highlight ONLY the target word forms, nothing else.

        OUTPUT FORMAT (STRICT):
        Return ONLY valid JSON with the following structure:

        {{
        "content": "Story text in {target_lang} with <b></b> tags",
        "translation": "Full translation of the story into {native_lang}",
        "highlighted_words": [
            "form1",
            "form2",
            "form3"
        ]
        }}

        ADDITIONAL RULES:
        - The "highlighted_words" array must contain ONLY the exact grammatical forms of "{word}" used in the story.
        - Do NOT include duplicates.
        - Do NOT include explanations, comments, markdown, or extra text.
        - Output MUST be valid JSON and nothing else.
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
            model="llama-3.3-70b-versatile", # Using Llama 3.3 for generation
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        
        response_content = chat_completion.choices[0].message.content
        return json.loads(response_content)
        
    except Exception as e:
        logger.error(f"Error generating story: {e}")
        raise e
