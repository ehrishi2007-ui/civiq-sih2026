"""
CiviQ M4 - Official Document Ingestion & Gemini File API Service.

Responsible for:
1. Discovering and validating approved MVP policy PDFs.
2. Registering and uploading PDFs via the modern official Gemini File API (google-genai).
3. Maintaining an idempotent runtime registry in uploaded_files.json.
4. Detecting stale/expired handles and re-uploading when necessary.
5. Providing document handles for downstream grounded RAG (M5).

Important:
- Uses ONLY `from google import genai`.
- Never hardcodes API keys.
- AI/Gemini does NOT evaluate citizen eligibility.
"""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Set

from google import genai
from api.config import settings

# Approved MVP Policy Documents (Exactly 6)
APPROVED_MVP_PDFS: Set[str] = {
    "APY.pdf",
    "PM-KISAN.pdf",
    "PMEGP.pdf",
    "PMSS 2023-24.pdf",
    "PMSS 2026-27.pdf",
    "StandupIndia.pdf",
}

# Explicitly excluded from MVP scope
EXCLUDED_PDFS: Set[str] = {
    "Sukanya_Samriddhi.pdf",
}


class PDFServiceError(Exception):
    """Base exception for CiviQ PDF service operations."""
    pass


class MissingPDFError(PDFServiceError):
    """Raised when one or more required MVP policy PDFs are missing from disk."""
    pass


class GeminiAuthError(PDFServiceError):
    """Raised when GEMINI_API_KEY is not configured."""
    pass


class GeminiUploadError(PDFServiceError):
    """Raised when uploading a document to Gemini File API fails."""
    pass


class RegistryError(PDFServiceError):
    """Raised when the registry file is corrupt or unreadable."""
    pass


def discover_approved_pdfs(pdf_dir: Optional[Path] = None) -> Dict[str, Path]:
    """
    Discovers only approved .pdf files in the raw PDFs directory.
    Validates that all six required MVP documents exist on disk.
    Explicitly ignores excluded PDFs (e.g. Sukanya_Samriddhi.pdf).
    """
    directory = pdf_dir or settings.RAW_PDFS_DIR

    if not directory.exists() or not directory.is_dir():
        raise MissingPDFError(f"Raw PDFs directory not found at: {directory}")

    # Discover all .pdf files in the directory
    found_files = {p.name: p for p in directory.glob("*.pdf")}

    # Filter out explicitly excluded files
    eligible_files = {
        name: path for name, path in found_files.items()
        if name in APPROVED_MVP_PDFS and name not in EXCLUDED_PDFS
    }

    # Verify that all 6 approved MVP PDFs are present
    missing = APPROVED_MVP_PDFS - set(eligible_files.keys())
    if missing:
        raise MissingPDFError(
            f"Missing required MVP policy PDFs: {sorted(list(missing))}. "
            f"Found: {sorted(list(eligible_files.keys()))}"
        )

    return eligible_files


def load_registry(registry_path: Optional[Path] = None) -> Dict[str, Dict[str, Any]]:
    """
    Loads the cached Gemini File API registry from disk.
    Returns an empty dict if the file does not exist or is empty.
    """
    path = registry_path or settings.UPLOADED_FILES_REGISTRY

    if not path.exists():
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {}
            data = json.loads(content)
            return data if isinstance(data, dict) else {}
    except json.JSONDecodeError as e:
        raise RegistryError(f"Malformed registry file at {path}: {str(e)}")
    except Exception as e:
        raise RegistryError(f"Failed to read registry file: {str(e)}")


def save_registry(registry: Dict[str, Dict[str, Any]], registry_path: Optional[Path] = None) -> None:
    """
    Persists the updated Gemini File API registry to disk.
    """
    path = registry_path or settings.UPLOADED_FILES_REGISTRY
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2)
    except Exception as e:
        raise RegistryError(f"Failed to write registry file: {str(e)}")


def get_gemini_client(api_key: Optional[str] = None) -> genai.Client:
    """
    Initializes and returns the modern official Google GenAI client.
    Fails safely if GEMINI_API_KEY is not configured.
    """
    key = api_key or os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY
    if not key or not key.strip():
        raise GeminiAuthError(
            "GEMINI_API_KEY environment variable is not configured. "
            "Please configure it to enable official document ingestion."
        )

    return genai.Client(api_key=key.strip())


def verify_cached_handle(client: Any, gemini_name: str) -> bool:
    """
    Verifies with the Gemini File API whether a cached handle is still active and valid.
    Returns False if the file is expired, deleted, or unavailable.
    """
    if not gemini_name:
        return False

    try:
        file_info = client.files.get(name=gemini_name)
        state = getattr(file_info, "state", None)
        if state is not None:
            state_str = str(getattr(state, "name", state)).upper()
            return state_str in {"ACTIVE", "PROCESSING", "STATE_UNSPECIFIED"}
        return True
    except Exception:
        # File expired, not found, or API rejected handle
        return False


def ingest_official_pdfs(
    api_key: Optional[str] = None,
    pdf_dir: Optional[Path] = None,
    registry_path: Optional[Path] = None,
    force_refresh: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """
    Idempotent official document ingestion pipeline:
    1. Validates presence of the 6 approved MVP PDFs.
    2. Loads the cached registry (uploaded_files.json).
    3. Reuses existing active Gemini handles without redundant uploads.
    4. Re-uploads missing, expired, or invalid handles.
    5. Saves updated registry and returns active handles.
    """
    approved_files = discover_approved_pdfs(pdf_dir)
    registry = load_registry(registry_path)
    client = get_gemini_client(api_key)

    active_handles: Dict[str, Dict[str, Any]] = {}
    updated = False

    for filename, file_path in sorted(approved_files.items()):
        cached_entry = registry.get(filename)
        is_valid = False

        if cached_entry and not force_refresh:
            gemini_name = cached_entry.get("gemini_name")
            if gemini_name and verify_cached_handle(client, gemini_name):
                is_valid = True
                active_handles[filename] = cached_entry

        if not is_valid:
            try:
                uploaded = client.files.upload(
                    file=str(file_path),
                    config={
                        "display_name": filename,
                        "mime_type": "application/pdf",
                    },
                )
                gemini_name = getattr(uploaded, "name", str(uploaded))
                uri = getattr(uploaded, "uri", "")
                now_iso = datetime.now(timezone.utc).isoformat()

                new_entry = {
                    "filename": filename,
                    "gemini_name": gemini_name,
                    "uri": uri,
                    "mime_type": "application/pdf",
                    "uploaded_at": now_iso,
                    "state": "ACTIVE",
                }
                registry[filename] = new_entry
                active_handles[filename] = new_entry
                updated = True
            except Exception as e:
                raise GeminiUploadError(f"Failed to upload '{filename}' to Gemini File API: {str(e)}")

    if updated or not (registry_path or settings.UPLOADED_FILES_REGISTRY).exists():
        save_registry(registry, registry_path)

    return active_handles


def get_official_pdf_handles(api_key: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """
    Retrieves the currently available Gemini File API handles for M5 RAG.
    If cached handles are valid, reuses them; otherwise performs ingestion.
    """
    registry = load_registry()
    client = get_gemini_client(api_key)

    # Check if all 6 MVP files are cached and active
    all_active = True
    for filename in APPROVED_MVP_PDFS:
        cached = registry.get(filename)
        if not cached or not verify_cached_handle(client, cached.get("gemini_name", "")):
            all_active = False
            break

    if all_active:
        return {name: registry[name] for name in APPROVED_MVP_PDFS if name in registry}

    # Run ingestion to refresh any missing or expired handles
    return ingest_official_pdfs(api_key=api_key)
