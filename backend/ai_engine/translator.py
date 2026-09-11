# translator.py
# Owned by: Dev 1 (Data & AI Architect)
# Purpose : Translate UI strings to Indian languages using Gemini Flash.
#           Replaces the Bhashini API dependency entirely.
#           Dev 2 calls translate_texts() from backend/api/routes/translate.py

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini once at module load
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
_model = genai.GenerativeModel("gemini-1.5-flash")

# ── In-memory cache ────────────────────────────────────────────────────────────
# Key format: "{target_lang}:{original_text}"  →  translated string
# Prevents calling Gemini twice for the same string in the same session.
_CACHE: dict[str, str] = {}

# ── Supported languages ────────────────────────────────────────────────────────
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

    Args:
        texts       : List of strings to translate (e.g. ["Eligible Schemes", "Apply Now"])
        target_lang : ISO 639-1 language code (e.g. "hi", "ta", "te")

    Returns:
        List of translated strings in the same order as input.
        Falls back to the original string if translation fails.
    """
    if target_lang == "en" or target_lang not in SUPPORTED_LANGUAGES:
        return texts  # No translation needed

    lang_name = SUPPORTED_LANGUAGES[target_lang]

    # ── Split into cached and uncached ────────────────────────────────────────
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

    # ── Batch-translate uncached strings in one Gemini call ───────────────────
    if uncached_texts:
        translated = _call_gemini(uncached_texts, lang_name)
        for idx, translated_text in zip(uncached_indices, translated):
            cache_key = f"{target_lang}:{texts[idx]}"
            _CACHE[cache_key] = translated_text
            results[idx] = translated_text

    return results


def _call_gemini(texts: list[str], lang_name: str) -> list[str]:
    """
    Internal: Call Gemini Flash to translate a batch of strings.
    Returns the original strings on any failure (safe fallback).
    """
    prompt = f"""You are a translation assistant for a government scheme platform.
Translate the following UI strings into {lang_name}.
Rules:
- Return ONLY a valid JSON array of translated strings.
- Preserve the exact same order as the input.
- Keep proper nouns (e.g. scheme names, ministry names) in English.
- Do not add explanations or extra text.

Input strings:
{json.dumps(texts, ensure_ascii=False)}"""

    try:
        response = _model.generate_content(prompt)
        # Strip markdown code fences if Gemini wraps the JSON
        raw = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        translated = json.loads(raw)
        if isinstance(translated, list) and len(translated) == len(texts):
            return translated
    except Exception:
        pass  # Fall through to safe fallback

    return texts  # Return originals if anything fails
