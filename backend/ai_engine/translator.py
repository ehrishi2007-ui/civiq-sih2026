# translator.py
# Owned by: Dev 1 (Data & AI Architect)
# Purpose : Translate UI strings to Indian languages using Gemini Flash with google-genai SDK.

import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

# In-memory translation cache
_CACHE: dict[str, str] = {}

SUPPORTED_LANGUAGES = {
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "bn": "Bengali",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "or": "Odia",
}

def translate_texts(texts: list[str], target_lang: str) -> list[str]:
    """
    Translate a list of UI strings into the target Indian language.
    """
    if target_lang == "en" or target_lang not in SUPPORTED_LANGUAGES:
        return texts

    lang_name = SUPPORTED_LANGUAGES[target_lang]

    results = [None] * len(texts)
    uncached_texts = []
    uncached_indices = []

    for i, text in enumerate(texts):
        cache_key = f"{target_lang}:{text}"
        if cache_key in _CACHE:
            results[i] = _CACHE[cache_key]
        else:
            uncached_texts.append(text)
            uncached_indices.append(i)

    if uncached_texts and client:
        translated = _call_gemini(uncached_texts, lang_name)
        for idx, translated_text in zip(uncached_indices, translated):
            cache_key = f"{target_lang}:{texts[idx]}"
            _CACHE[cache_key] = translated_text
            results[idx] = translated_text
    elif uncached_texts:
        for idx in uncached_indices:
            results[idx] = texts[idx]

    return results

def _call_gemini(texts: list[str], lang_name: str) -> list[str]:
    prompt = f"""You are a translation assistant for an Indian government scheme platform.
Translate the following UI strings into {lang_name}.
Rules:
- Return ONLY a valid JSON array of translated strings.
- Preserve the exact same order as the input.
- Keep proper nouns (e.g. scheme names, ministry names) in English.
- Do not add explanations or markdown quotes.

Input strings:
{json.dumps(texts, ensure_ascii=False)}"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        raw = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        translated = json.loads(raw)
        if isinstance(translated, list) and len(translated) == len(texts):
            return translated
    except Exception as e:
        print(f"Translation notice: {e}")

    return texts
