"""
Unit tests for CiviQ M4 - Official Document Ingestion & Gemini File API Service.

Validates:
1. Exactly 6 approved MVP PDFs are discovered and selected.
2. Sukanya_Samriddhi.pdf is explicitly excluded.
3. Missing required PDF raises MissingPDFError.
4. Registry loads safely (handles missing file, empty file, corrupt file).
5. Stale/invalid cached handles trigger re-upload.
6. Valid active cached handles are reused without redundant upload.
7. Missing GEMINI_API_KEY raises GeminiAuthError safely without network calls.
8. Ingestion returns all 6 document handles when valid.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from ai_engine.pdf_service import (
    APPROVED_MVP_PDFS,
    EXCLUDED_PDFS,
    GeminiAuthError,
    GeminiUploadError,
    MissingPDFError,
    RegistryError,
    discover_approved_pdfs,
    get_gemini_client,
    get_official_pdf_handles,
    ingest_official_pdfs,
    load_registry,
    save_registry,
    verify_cached_handle,
)


# =====================================================================
# 1. Exactly six MVP PDFs are selected
# =====================================================================
def test_exactly_six_mvp_pdfs_selected():
    assert len(APPROVED_MVP_PDFS) == 6
    approved = discover_approved_pdfs()
    assert len(approved) == 6
    assert set(approved.keys()) == APPROVED_MVP_PDFS


# =====================================================================
# 2. Sukanya_Samriddhi.pdf is explicitly excluded
# =====================================================================
def test_sukanya_samriddhi_excluded():
    assert "Sukanya_Samriddhi.pdf" in EXCLUDED_PDFS
    assert "Sukanya_Samriddhi.pdf" not in APPROVED_MVP_PDFS
    approved = discover_approved_pdfs()
    assert "Sukanya_Samriddhi.pdf" not in approved


# =====================================================================
# 3. Missing required PDF is detected
# =====================================================================
def test_missing_required_pdf_detected(tmp_path):
    # Create directory with only 5 of the 6 files
    for filename in list(APPROVED_MVP_PDFS)[:5]:
        (tmp_path / filename).write_text("fake pdf content")

    with pytest.raises(MissingPDFError) as exc_info:
        discover_approved_pdfs(pdf_dir=tmp_path)

    assert "Missing required MVP policy PDFs" in str(exc_info.value)


# =====================================================================
# 4. Registry can be loaded and saved safely
# =====================================================================
def test_registry_load_and_save_safe(tmp_path):
    reg_file = tmp_path / "test_uploaded.json"

    # Non-existent registry returns empty dict
    assert load_registry(registry_path=reg_file) == {}

    # Empty file returns empty dict
    reg_file.write_text("")
    assert load_registry(registry_path=reg_file) == {}

    # Valid data saves and loads correctly
    sample_data = {
        "APY.pdf": {
            "filename": "APY.pdf",
            "gemini_name": "files/apy-123",
            "state": "ACTIVE",
        }
    }
    save_registry(sample_data, registry_path=reg_file)
    loaded = load_registry(registry_path=reg_file)
    assert loaded == sample_data

    # Corrupt JSON raises RegistryError
    reg_file.write_text("{corrupt: json")
    with pytest.raises(RegistryError):
        load_registry(registry_path=reg_file)


# =====================================================================
# 5. Invalid/stale cached handles trigger re-upload behavior
# =====================================================================
def test_stale_handle_triggers_reupload(tmp_path):
    reg_file = tmp_path / "registry.json"
    # Create cached entry with handle that fails verification
    initial_registry = {
        "APY.pdf": {
            "filename": "APY.pdf",
            "gemini_name": "files/stale-handle",
            "state": "ACTIVE",
        }
    }
    save_registry(initial_registry, registry_path=reg_file)

    mock_client = MagicMock()
    # files.get raises exception (file expired/deleted in Gemini)
    mock_client.files.get.side_effect = Exception("File not found")

    mock_uploaded = MagicMock()
    mock_uploaded.name = "files/new-fresh-handle"
    mock_uploaded.uri = "https://gemini.example/files/new"
    mock_client.files.upload.return_value = mock_uploaded

    with patch("ai_engine.pdf_service.get_gemini_client", return_value=mock_client):
        handles = ingest_official_pdfs(
            api_key="test-api-key",
            registry_path=reg_file,
        )

    # All 6 must be uploaded since cached was invalid and others were missing
    assert mock_client.files.upload.call_count == 6
    assert handles["APY.pdf"]["gemini_name"] == "files/new-fresh-handle"

    # Verify updated registry was saved
    updated_reg = load_registry(reg_file)
    assert updated_reg["APY.pdf"]["gemini_name"] == "files/new-fresh-handle"


# =====================================================================
# 6. Valid cached handles are reused without redundant upload
# =====================================================================
def test_valid_cached_handles_reused(tmp_path):
    reg_file = tmp_path / "registry.json"
    # Populate registry with all 6 valid files
    mock_registry = {}
    for filename in APPROVED_MVP_PDFS:
        mock_registry[filename] = {
            "filename": filename,
            "gemini_name": f"files/{filename}-cached",
            "uri": f"https://gemini.example/files/{filename}",
            "state": "ACTIVE",
        }
    save_registry(mock_registry, registry_path=reg_file)

    mock_client = MagicMock()
    mock_active_file = MagicMock()
    mock_active_file.state.name = "ACTIVE"
    mock_client.files.get.return_value = mock_active_file

    with patch("ai_engine.pdf_service.get_gemini_client", return_value=mock_client):
        handles = ingest_official_pdfs(
            api_key="test-api-key",
            registry_path=reg_file,
        )

    # files.upload must NOT be called since all 6 handles were active
    assert mock_client.files.upload.call_count == 0
    assert len(handles) == 6
    assert mock_client.files.get.call_count == 6
    assert handles["PM-KISAN.pdf"]["gemini_name"] == "files/PM-KISAN.pdf-cached"


# =====================================================================
# 7. Missing GEMINI_API_KEY is handled safely
# =====================================================================
def test_missing_gemini_api_key_handled_safely(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr("ai_engine.pdf_service.settings.GEMINI_API_KEY", "")
    with pytest.raises(GeminiAuthError) as exc_info:
        get_gemini_client(api_key=None)

    assert "GEMINI_API_KEY environment variable is not configured" in str(exc_info.value)


# =====================================================================
# 8. Service returns expected 6 document handles when ingestion succeeds
# =====================================================================
def test_service_returns_expected_six_handles(tmp_path):
    reg_file = tmp_path / "registry.json"

    mock_client = MagicMock()
    mock_client.files.get.side_effect = Exception("Not found")

    def make_upload_mock(file, config):
        m = MagicMock()
        m.name = f"files/{config['display_name']}-uploaded"
        m.uri = f"https://gemini.example/{config['display_name']}"
        return m

    mock_client.files.upload.side_effect = make_upload_mock

    with patch("ai_engine.pdf_service.get_gemini_client", return_value=mock_client):
        handles = ingest_official_pdfs(
            api_key="mock-api-key",
            registry_path=reg_file,
        )

    assert len(handles) == 6
    for filename in APPROVED_MVP_PDFS:
        assert filename in handles
        assert handles[filename]["gemini_name"] == f"files/{filename}-uploaded"
        assert handles[filename]["state"] == "ACTIVE"


# =====================================================================
# 9. verify_cached_handle helper behavior
# =====================================================================
def test_verify_cached_handle_states():
    mock_client = MagicMock()

    # Active state -> True
    mock_file_active = MagicMock()
    mock_file_active.state = "ACTIVE"
    mock_client.files.get.return_value = mock_file_active
    assert verify_cached_handle(mock_client, "files/1") is True

    # Empty handle string -> False
    assert verify_cached_handle(mock_client, "") is False

    # Exception from API -> False
    mock_client.files.get.side_effect = Exception("API connection error")
    assert verify_cached_handle(mock_client, "files/error") is False
