"""
Unit and Contract Tests for CiviQ Milestone 8:
Multi-Language Translation (Google Cloud Translation API) & Safe Supabase Client Adapter.
"""

from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient

from api.main import app
from ai_engine.translator import (
    SUPPORTED_LANGUAGES,
    VALID_TARGET_LANGUAGES,
    _CACHE,
    clear_cache,
    translate_text,
    translate_text_with_meta,
    translate_texts,
    validate_target_language,
)
from ai_engine.db_client import (
    get_client,
    is_connected,
    reset_client,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_cache_and_db():
    """Ensure clean cache and DB state for every test."""
    clear_cache()
    reset_client()
    yield
    clear_cache()
    reset_client()


# ==========================================
# 1. Supported Language Validation
# ==========================================

def test_supported_language_validation():
    """Verify all 10 approved Indian languages + English pass validation."""
    expected_indian_langs = ["hi", "ta", "te", "bn", "kn", "ml", "mr", "gu", "pa", "or"]
    for lang in expected_indian_langs:
        assert lang in SUPPORTED_LANGUAGES
        assert validate_target_language(lang) == lang
        assert validate_target_language(lang.upper()) == lang  # case insensitivity

    assert "en" in VALID_TARGET_LANGUAGES
    assert validate_target_language("en") == "en"
    assert validate_target_language("EN ") == "en"


# ==========================================
# 2. Unsupported Language Rejection
# ==========================================

def test_unsupported_language_rejection():
    """Verify unsupported languages raise ValueError and return HTTP 422 in API."""
    unsupported = ["fr", "de", "es", "zh", "xx", "unknown"]
    for lang in unsupported:
        with pytest.raises(ValueError) as excinfo:
            validate_target_language(lang)
        assert f"Unsupported target language '{lang}'" in str(excinfo.value)

    # API validation test
    resp = client.post("/api/v1/translate", json={"text": "Hello", "target_language": "fr"})
    assert resp.status_code == 422
    assert "Unsupported target language" in resp.json()["detail"]


# ==========================================
# 3. English No-op
# ==========================================

def test_english_noop():
    """Verify target_language='en' returns original text without any external API calls."""
    with patch("ai_engine.translator._call_google_translate_api") as mock_api:
        text = "Find the government schemes you're eligible for"
        result = translate_text(text, "en")
        assert result == text
        mock_api.assert_not_called()

        # Batch interface test
        batch_result = translate_texts([text, "Another string"], "en")
        assert batch_result == [text, "Another string"]
        mock_api.assert_not_called()


# ==========================================
# 4. Empty Input Handling
# ==========================================

def test_empty_input_handling():
    """Verify empty or whitespace strings return immediately without calling Google API."""
    with patch("ai_engine.translator._call_google_translate_api") as mock_api:
        assert translate_text("", "hi") == ""
        assert translate_text("   ", "hi") == "   "
        mock_api.assert_not_called()

        # API endpoint handles whitespace/empty string gracefully
        resp = client.post("/api/v1/translate", json={"text": "   ", "target_language": "hi"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["translated_text"] == "   "
        assert data["target_language"] == "hi"
        assert data["detected_source_language"] == "en"


# ==========================================
# 5. Translation Cache Hit
# ==========================================

def test_translation_cache_hit():
    """Verify repeated translations hit in-memory cache without secondary API calls and preserve detected language."""
    mock_response = [{"translatedText": "सरकारी योजनाएं", "detectedSourceLanguage": "en"}]
    with patch("ai_engine.translator._call_google_translate_api", return_value=mock_response) as mock_api:
        text = "Government Schemes"

        # First call: cache miss, invokes API
        first_call = translate_text(text, "hi")
        assert first_call == "सरकारी योजनाएं"
        assert mock_api.call_count == 1
        assert "hi:Government Schemes" in _CACHE

        # Second call: cache hit, returns from _CACHE
        second_call, cached_source = translate_text_with_meta(text, "hi")
        assert second_call == "सरकारी योजनाएं"
        assert cached_source == "en"
        assert mock_api.call_count == 1  # count did not increase!


# ==========================================
# 6. Google API Call Structure and Mock
# ==========================================

def test_google_api_call_structure():
    """Verify Google API HTTP call sends correct URL, query params, and JSON payload."""
    with patch("ai_engine.translator.settings.GOOGLE_TRANSLATE_API_KEY", "mock-translate-key"):
        with patch("httpx.post") as mock_post:
            mock_post.return_value = MagicMock(
                status_code=200,
                json=lambda: {
                    "data": {
                        "translations": [
                            {"translatedText": "नमस्ते", "detectedSourceLanguage": "en"}
                        ]
                    }
                },
            )

            res = translate_text("Hello", "hi")
            assert res == "नमस्ते"

            mock_post.assert_called_once()
            call_args = mock_post.call_args
            assert call_args[0][0] == "https://translation.googleapis.com/language/translate/v2"
            assert call_args[1]["params"] == {"key": "mock-translate-key"}
            assert call_args[1]["json"] == {
                "q": ["Hello"],
                "target": "hi",
                "format": "text",
            }


# ==========================================
# 7. Successful API Response Parsing & HTML Unescape
# ==========================================

def test_successful_api_response_parsing_and_html_unescape():
    """Verify parsing handles HTML entities (e.g. &quot;, &#39;) and multiple texts."""
    mock_translations = [
        {"translatedText": "&quot;प्रधान मंत्री किसान सम्मान निधि&quot;", "detectedSourceLanguage": "en"},
        {"translatedText": "किसान का परिवार", "detectedSourceLanguage": "en"},
    ]
    with patch("ai_engine.translator._call_google_translate_api", return_value=mock_translations):
        results = translate_texts(['"PM-KISAN"', "Farmer's family"], "hi")
        assert results[0] == '"प्रधान मंत्री किसान सम्मान निधि"'
        assert results[1] == "किसान का परिवार"


# ==========================================
# 8. API Failure Fallback
# ==========================================

def test_api_failure_fallback_does_not_crash_or_cache():
    """Verify API 500 error triggers fallback to original text and does NOT cache failure."""
    with patch("ai_engine.translator._call_google_translate_api", return_value=None) as mock_api:
        text = "Application Status"
        result = translate_text(text, "ta")

        # Returns original text
        assert result == text
        # Must not cache failed result
        assert "ta:Application Status" not in _CACHE

        # Second call still attempts API because failure was not cached
        translate_text(text, "ta")
        assert mock_api.call_count == 2


# ==========================================
# 9. Missing API Key Fallback & Conservative Language Detection
# ==========================================

def test_missing_api_key_fallback():
    """Verify unconfigured GOOGLE_TRANSLATE_API_KEY gracefully returns source text and conservative language."""
    with patch("ai_engine.translator.settings.GOOGLE_TRANSLATE_API_KEY", ""):
        # ASCII text defaults to "en"
        text = "Check Eligibility"
        result, source_lang = translate_text_with_meta(text, "te")
        assert result == text
        assert source_lang == "en"

        # Non-ASCII text conservatively reports "und" rather than fabricating "en"
        hindi_text = "मेरी पात्रता क्या है?"
        h_result, h_source = translate_text_with_meta(hindi_text, "ta")
        assert h_result == hindi_text
        assert h_source == "und"


# ==========================================
# 10. POST /api/v1/translate Contract
# ==========================================

def test_post_translate_contract():
    """Verify POST /api/v1/translate matches frontend expectations."""
    mock_response = [{"translatedText": "अपनी पात्रता जांचें", "detectedSourceLanguage": "en"}]
    with patch("ai_engine.translator._call_google_translate_api", return_value=mock_response):
        payload = {
            "text": "Check your eligibility",
            "target_language": "hi",
        }
        resp = client.post("/api/v1/translate", json=payload)
        assert resp.status_code == 200
        data = resp.json()

        assert "translated_text" in data
        assert data["translated_text"] == "अपनी पात्रता जांचें"
        assert data["target_language"] == "hi"
        assert data["detected_source_language"] == "en"


# ==========================================
# 11. Supabase Missing Credentials Does Not Crash
# ==========================================

def test_supabase_missing_credentials_does_not_crash():
    """Verify Supabase adapter returns None and is_connected() is False without credentials."""
    with patch("ai_engine.db_client.settings.SUPABASE_URL", ""):
        with patch("ai_engine.db_client.settings.SUPABASE_KEY", ""):
            reset_client()
            client_inst = get_client()
            assert client_inst is None
            assert is_connected() is False


# ==========================================
# 12. Supabase get_client() Idempotency and Unavailable Package
# ==========================================

def test_supabase_get_client_idempotent_and_safe_when_uninstalled():
    """Verify repeated get_client() calls are cached and safe when package is uninstalled."""
    with patch("ai_engine.db_client._SUPABASE_AVAILABLE", False):
        with patch("ai_engine.db_client.settings.SUPABASE_URL", "https://xyz.supabase.co"):
            with patch("ai_engine.db_client.settings.SUPABASE_KEY", "anon-key"):
                reset_client()
                assert get_client() is None
                assert is_connected() is False

                # Second call reuses initialized None
                assert get_client() is None


# ==========================================
# 13. Supabase Mocked Initialization (No Live DB Calls in Tests)
# ==========================================

def test_supabase_mocked_initialization_no_live_calls():
    """Verify Supabase initialization is cleanly mockable and never connects to live services."""
    mock_supabase_client = MagicMock()
    mock_create_client = MagicMock(return_value=mock_supabase_client)

    with patch("ai_engine.db_client._SUPABASE_AVAILABLE", True):
        with patch("ai_engine.db_client.create_client", mock_create_client):
            with patch("ai_engine.db_client.settings.SUPABASE_URL", "https://project.supabase.co"):
                with patch("ai_engine.db_client.settings.SUPABASE_KEY", "secret-test-key"):
                    reset_client()
                    client_inst = get_client()
                    assert client_inst is mock_supabase_client
                    assert is_connected() is True
                    mock_create_client.assert_called_once_with(
                        "https://project.supabase.co", "secret-test-key"
                    )
