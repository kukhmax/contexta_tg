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
    
    # Общий системный промпт (Prompt)
    prompt = f"""
        You are an experienced professional language teacher and curriculum designer.

        TASK:
        Create a short, coherent story in {target_lang} suitable strictly for CEFR level {level}.

        TARGET WORD / PHRASE:
        "{word}"

        GRAMMAR REQUIREMENTS (VERY IMPORTANT):
        - You MUST use the target word "{word}" in AT LEAST 5 DIFFERENT grammatical forms.
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
        - Length: 100–150 words.
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
        # Логика выбора провайдера AI (Groq или Gemini)
        if settings.IS_GEMINI:
            import google.generativeai as genai
            
            if not settings.GEMINI_API_KEY:
                raise ValueError("API Key for Gemini is not configured / Ключ Gemini API не настроен")
                
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.0-flash') # Используем быструю и новую модель
            
            # Gemini иногда любит добавлять markdown блоки ```json ... ```, нужно парсить аккуратно
            # Добавляем инструкцию для JSON формата в chat
            response = model.generate_content(
                f"You are a helpful assistant that outputs only valid JSON.\n{prompt}",
                generation_config={"response_mime_type": "application/json"}
            )
            
            response_content = response.text
            return json.loads(response_content)
            
        else:
            # Использование Groq API (по умолчанию)
            if not settings.GROQ_API_KEY:
                raise ValueError("API Key for Groq is not configured / Ключ Groq API не настроен")

            client = Groq(api_key=settings.GROQ_API_KEY)
            
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
                model="llama-3.3-70b-versatile", # Используем Llama 3.3
                temperature=0.7,
                response_format={"type": "json_object"},
            )
            
            response_content = chat_completion.choices[0].message.content
            return json.loads(response_content)
        
    except Exception as e:
        logger.error(f"Error generating story: {e}")
        raise e

async def enrich_word_info(word: str, context: str, native_lang: str) -> dict:
    """
    Получает перевод слова и спряжения (если это глагол) через AI.
    """
    prompt = f"""
    You are a language teacher. 
    Analyze the word "{word}" in the following context: "{context}".
    
    1. Translate the word "{word}" into {native_lang}.
    2. Determine if "{word}" acts as a VERB in this context.
    3. IF it is a VERB, provide its PRESENT TENSE conjugations (I, You, He/She, We, They).
    4. IF it is NOT a verb, return null for conjugations.

    OUTPUT FORMAT (JSON ONLY):
    {{
        "translation": "Translation in {native_lang}",
        "is_verb": true/false,
        "conjugations": "I am, You are, He is..." (or null if not a verb or not applicable)
    }}
    """
    
    try:
        if settings.IS_GEMINI:
            import google.generativeai as genai
            if not settings.GEMINI_API_KEY:
                # Fallback empty
                return {"translation": None, "context": context}

            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(
                 f"You are a helpful assistant that outputs only valid JSON.\n{prompt}",
                 generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
            
        else:
            if not settings.GROQ_API_KEY:
                return {"translation": None, "context": context}

            client = Groq(api_key=settings.GROQ_API_KEY)
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that outputs only JSON."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                response_format={"type": "json_object"},
            )
            return json.loads(chat_completion.choices[0].message.content)

    except Exception as e:
        logger.error(f"Error enriching word: {e}")
        return {"translation": None, "is_verb": False, "conjugations": None}
