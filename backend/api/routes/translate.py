"""
Translation route for CiviQ API.
Conforms strictly to CiviQ frontend translation contract.
"""

from fastapi import APIRouter, HTTPException, status
try:
    from ai_engine.translator import (
        VALID_TARGET_LANGUAGES,
        translate_text_with_meta,
    )
except ImportError:
    from backend.ai_engine.translator import (
        VALID_TARGET_LANGUAGES,
        translate_text_with_meta,
    )
from ..schemas import TranslateRequest, TranslateResponse

router = APIRouter(prefix="/translate", tags=["translate"])


@router.post("", response_model=TranslateResponse)
async def translate_endpoint(request: TranslateRequest) -> TranslateResponse:
    """
    Translates provided text into the target Indian language using Google Cloud Translation API.
    Conforms to frontend contract:
    Request: {"text": str, "target_language": str}
    Response: {"translated_text": str, "target_language": str, "detected_source_language": str}
    """
    target_lang = request.target_language.lower().strip()
    if target_lang not in VALID_TARGET_LANGUAGES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported target language '{request.target_language}'. Supported languages: {sorted(VALID_TARGET_LANGUAGES)}",
        )

    # Empty or whitespace input: controlled no-op response
    if not request.text or not request.text.strip():
        return TranslateResponse(
            translated_text=request.text,
            target_language=target_lang,
            detected_source_language="en",
        )

    translated_text, detected_source = translate_text_with_meta(request.text, target_lang)

    return TranslateResponse(
        translated_text=translated_text,
        target_language=target_lang,
        detected_source_language=detected_source,
    )
