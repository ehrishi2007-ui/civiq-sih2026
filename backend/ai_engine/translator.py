"""
Translation Engine for CiviQ.
Provides multi-language translation for Indian vernaculars using Google Cloud Translation API.
Adapts Dev1's cache architecture, batch translation interface, and resilient fallbacks.
"""

import html
import logging
from typing import Dict, List, Optional, Tuple
import httpx

try:
    from api.config import settings
except ImportError:
    from backend.api.config import settings

logger = logging.getLogger(__name__)

# Supported Indian languages + English as default/no-op
SUPPORTED_LANGUAGES: Dict[str, str] = {
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

VALID_TARGET_LANGUAGES: set[str] = set(SUPPORTED_LANGUAGES.keys()) | {"en"}

# In-memory translation cache (keyed by f"{target_lang}:{text}")
_CACHE: Dict[str, str] = {}
_SOURCE_LANG_CACHE: Dict[str, str] = {}


def _is_ascii(text: str) -> bool:
    """Checks if text contains only ASCII characters (standard English representation)."""
    try:
        text.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def clear_cache() -> None:
    """Clears the in-memory translation cache (primarily for tests)."""
    _CACHE.clear()
    _SOURCE_LANG_CACHE.clear()


def validate_target_language(target_lang: str) -> str:
    """
    Validates and normalizes target language code.
    Raises ValueError if unsupported.
    """
    normalized = target_lang.lower().strip()
    if normalized not in VALID_TARGET_LANGUAGES:
        raise ValueError(
            f"Unsupported target language '{target_lang}'. "
            f"Supported languages: {sorted(VALID_TARGET_LANGUAGES)}"
        )
    return normalized


def _call_google_translate_api(texts: List[str], target_lang: str) -> Optional[List[Dict[str, str]]]:
    """
    Invokes Google Cloud Translation API v2 REST endpoint.
    Returns list of translation objects or None on failure/missing key.
    """
    api_key = settings.GOOGLE_TRANSLATE_API_KEY
    if not api_key:
        logger.warning("GOOGLE_TRANSLATE_API_KEY is not configured; using offline fallback.")
        return None

    url = "https://translation.googleapis.com/language/translate/v2"
    params = {"key": api_key}
    payload = {
        "q": texts,
        "target": target_lang,
        "format": "text",
    }

    try:
        response = httpx.post(url, params=params, json=payload, timeout=10.0)
        if response.status_code == 200:
            data = response.json()
            translations = data.get("data", {}).get("translations", [])
            if isinstance(translations, list) and len(translations) == len(texts):
                return translations
            logger.warning("Unexpected translations count from Google Translation API: %s", data)
            return None
        else:
            logger.warning(
                "Google Translation API returned error status %d: %s",
                response.status_code,
                response.text,
            )
            return None
    except Exception as exc:
        logger.warning("Google Translation API request error: %s", exc)
        return None


def translate_text(text: str, target_lang: str) -> str:
    """
    Translate a single text string to the target language.
    Returns original text if target_lang is 'en', text is empty/whitespace,
    or if translation fails/is unconfigured.
    """
    translated_text, _ = translate_text_with_meta(text, target_lang)
    return translated_text


def translate_text_with_meta(text: str, target_lang: str) -> Tuple[str, str]:
    """
    Translate a single text string to the target language, returning
    (translated_text, detected_source_language).
    """
    norm_target = validate_target_language(target_lang)

    # Empty or whitespace: return unchanged with conservative detection
    if not text or not text.strip():
        return text, ("en" if _is_ascii(text) else "und")

    # No-op English
    if norm_target == "en":
        return text, ("en" if _is_ascii(text) else "und")

    cache_key = f"{norm_target}:{text}"
    if cache_key in _CACHE:
        cached_detected = _SOURCE_LANG_CACHE.get(cache_key, "en" if _is_ascii(text) else "und")
        return _CACHE[cache_key], cached_detected

    translations = _call_google_translate_api([text], norm_target)
    if translations:
        item = translations[0]
        translated = html.unescape(item.get("translatedText", text))
        detected = item.get("detectedSourceLanguage") or ("en" if _is_ascii(text) else "und")
        _CACHE[cache_key] = translated
        _SOURCE_LANG_CACHE[cache_key] = detected
        return translated, detected

    # Fallback: return original text without caching failure; conservative language detection
    fallback_detected = "en" if _is_ascii(text) else "und"
    return text, fallback_detected


def translate_texts(texts: List[str], target_lang: str) -> List[str]:
    """
    Translate a list of UI strings into the target Indian language.
    Adapts Dev1's batched translation pattern with Google Cloud Translation API.
    """
    norm_target = validate_target_language(target_lang)

    if not texts:
        return []

    # No-op English
    if norm_target == "en":
        return list(texts)

    results: List[Optional[str]] = [None] * len(texts)
    uncached_texts: List[str] = []
    uncached_indices: List[int] = []

    for i, text in enumerate(texts):
        if not text or not text.strip():
            results[i] = text
            continue

        cache_key = f"{norm_target}:{text}"
        if cache_key in _CACHE:
            results[i] = _CACHE[cache_key]
        else:
            uncached_texts.append(text)
            uncached_indices.append(i)

    if uncached_texts:
        api_results = _call_google_translate_api(uncached_texts, norm_target)
        if api_results and len(api_results) == len(uncached_texts):
            for idx, item in zip(uncached_indices, api_results):
                orig_text = texts[idx]
                translated = html.unescape(item.get("translatedText", orig_text))
                cache_key = f"{norm_target}:{orig_text}"
                _CACHE[cache_key] = translated
                _SOURCE_LANG_CACHE[cache_key] = item.get("detectedSourceLanguage") or ("en" if _is_ascii(orig_text) else "und")
                results[idx] = translated
        else:
            # Fallback for all uncached items without caching errors
            for idx in uncached_indices:
                results[idx] = texts[idx]

    return [r if r is not None else texts[idx] for idx, r in enumerate(results)]
