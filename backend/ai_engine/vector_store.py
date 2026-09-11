"""
CiviQ Vector Store Compatibility Layer.

Dev1 implemented vector_store.py as an upload script to the Gemini File API.
Our authoritative document ingestion is handled by `pdf_service.py`.
This module provides backward-compatibility functions delegating to `pdf_service.py`
to avoid duplicate upload logic.
"""

from typing import Any, Dict, List, Optional

try:
    from .pdf_service import (
        get_gemini_client,
        get_official_pdf_handles,
        ingest_official_pdfs,
    )
except ImportError:
    from ai_engine.pdf_service import (
        get_gemini_client,
        get_official_pdf_handles,
        ingest_official_pdfs,
    )


def get_uploaded_files(api_key: Optional[str] = None) -> List[Any]:
    """
    Backward-compatible alias returning active Gemini File objects.
    Delegates to pdf_service.get_official_pdf_handles without duplicating upload logic.
    """
    try:
        client = get_gemini_client(api_key)
        handles_dict = get_official_pdf_handles(api_key=api_key)
        files = []
        for item in handles_dict.values():
            gemini_name = item.get("gemini_name")
            if gemini_name:
                try:
                    f = client.files.get(name=gemini_name)
                    files.append(f)
                except Exception:
                    pass
        return files
    except Exception:
        return []


def upload_all_pdfs(pdf_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Backward-compatible alias delegating to pdf_service.ingest_official_pdfs.
    """
    return ingest_official_pdfs()
