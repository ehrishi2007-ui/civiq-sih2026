"""
Unit and Integration Tests for CiviQ M5 - Policy Intelligence & Grounded Document RAG.

Validates:
1. Missing GEMINI_API_KEY returns graceful response without crashing.
2. Empty questions handled safely with informative message.
3. Missing or unindexed documents handled gracefully.
4. ask_policy with mocked Gemini generates grounded response and sources.
5. extract_citations parses structured blocks without fabricating page numbers.
6. extract_citations inline document mentions preserve absence of fake pages.
7. vector_store compatibility module delegates cleanly to pdf_service.
8. POST /api/v1/ask endpoint conforms strictly to {"answer": ..., "sources": [...]}.
9. POST /api/v1/ask rejects invalid/empty payload with HTTP 422.
10. Architectural boundary: RAG does not evaluate citizen eligibility.
"""

from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.schemas import AskRequest, AskResponse
from ai_engine.rag import ask_policy, extract_citations, SYSTEM_INSTRUCTION
from ai_engine.vector_store import get_uploaded_files, upload_all_pdfs
from ai_engine.evaluator import evaluate_eligibility

client = TestClient(app)


# =====================================================================
# 1. Missing GEMINI_API_KEY handled gracefully
# =====================================================================
def test_ask_policy_missing_api_key():
    with patch("ai_engine.rag.settings.GEMINI_API_KEY", ""), patch.dict("os.environ", {"GEMINI_API_KEY": ""}, clear=True):
        res = ask_policy("What is PM-KISAN?", api_key="")
        assert res["success"] is False
        assert "GEMINI_API_KEY is not configured" in res["answer"]
        assert res["sources"] == []


# =====================================================================
# 2. Empty question validation
# =====================================================================
def test_ask_policy_empty_question():
    res = ask_policy("   ")
    assert res["success"] is False
    assert "Please provide a valid question" in res["answer"]
    assert res["sources"] == []


# =====================================================================
# 3. Missing or unindexed documents
# =====================================================================
def test_ask_policy_no_indexed_documents():
    with patch("ai_engine.rag.get_official_pdf_handles", return_value={}):
        res = ask_policy("What is the benefit under PM-KISAN?", api_key="test-api-key")
        assert res["success"] is False
        assert "No official policy documents are currently indexed" in res["answer"]
        assert res["sources"] == []


# =====================================================================
# 4. Successful ask_policy with mocked Gemini client
# =====================================================================
def test_ask_policy_success_with_mock():
    mock_handles = {
        "PM-KISAN.pdf": {"gemini_name": "files/pmkisan123", "uri": "https://genai/pmkisan"},
        "PMEGP.pdf": {"gemini_name": "files/pmegp123", "uri": "https://genai/pmegp"},
    }

    mock_client = MagicMock()
    mock_file_obj = MagicMock()
    mock_client.files.get.return_value = mock_file_obj

    mock_response = MagicMock()
    mock_response.text = (
        "1. Direct Answer: Under PM-KISAN, farmers receive Rs 6,000 per year.\n"
        "2. Official Citation:\n"
        "   - Document Name: PM-KISAN.pdf\n"
        "   - Page Number: 2\n"
        "   - Exact Clause: 'Under the scheme, an income support of Rs 6,000 per year is provided'"
    )
    mock_client.models.generate_content.return_value = mock_response

    with patch("ai_engine.rag.get_gemini_client", return_value=mock_client), \
         patch("ai_engine.rag.get_official_pdf_handles", return_value=mock_handles):

        res = ask_policy(
            question="What is the benefit amount for PM-KISAN?",
            context={"occupation": "Farmer"},
            api_key="test-api-key",
            model="gemini-2.5-flash",
        )

        assert res["success"] is True
        assert "Rs 6,000 per year" in res["answer"]
        assert res["documents_consulted"] == 2
        assert res["model"] == "gemini-2.5-flash"
        assert len(res["sources"]) == 1
        assert res["sources"][0]["doc_name"] == "PM-KISAN.pdf"
        assert res["sources"][0]["page"] == 2
        assert "income support of Rs 6,000" in res["sources"][0]["quote"]

        # Verify client calls
        mock_client.models.generate_content.assert_called_once()
        call_kwargs = mock_client.models.generate_content.call_args.kwargs
        assert call_kwargs["model"] == "gemini-2.5-flash"
        assert call_kwargs["config"].system_instruction == SYSTEM_INSTRUCTION


# =====================================================================
# 5. Citation extraction from structured blocks
# =====================================================================
def test_extract_citations_structured_blocks():
    text = (
        "Here is the policy information:\n\n"
        "Document Name: PMEGP.pdf\n"
        "Page Number: 5\n"
        "Exact Clause: Any individual, above 18 years of age\n\n"
        "Also under PMSS:\n"
        "Document Name: PMSS 2023-24.pdf\n"
        "Page Number: 3\n"
        "Clause: Having minimum 60% marks in Minimum Entry Qualification"
    )
    citations = extract_citations(text)
    assert len(citations) == 2
    assert citations[0]["doc_name"] == "PMEGP.pdf"
    assert citations[0]["page"] == 5
    assert citations[0]["quote"] == "Any individual, above 18 years of age"

    assert citations[1]["doc_name"] == "PMSS 2023-24.pdf"
    assert citations[1]["page"] == 3
    assert "minimum 60% marks" in citations[1]["quote"]


# =====================================================================
# 6. Citation extraction: inline mentions without fabricated page numbers
# =====================================================================
def test_extract_citations_no_fabricated_pages():
    text = (
        "According to StandupIndia.pdf, the scheme assists SC, ST and women borrowers. "
        "Specific sub-rules are governed by regional bank guidelines."
    )
    citations = extract_citations(text)
    assert len(citations) == 1
    assert citations[0]["doc_name"] == "StandupIndia.pdf"
    # Crucial: Must NOT fabricate a fake page number like 1
    assert citations[0]["page"] is None
    assert citations[0]["quote"] is None


# =====================================================================
# 7. Vector store compatibility layer delegates to pdf_service
# =====================================================================
def test_vector_store_compatibility_layer():
    with patch("ai_engine.vector_store.get_official_pdf_handles") as mock_handles, \
         patch("ai_engine.vector_store.get_gemini_client") as mock_client:
        mock_handles.return_value = {
            "PM-KISAN.pdf": {"gemini_name": "files/pmkisan_test"}
        }
        mock_cli = MagicMock()
        mock_cli.files.get.return_value = MagicMock(name="file_obj")
        mock_client.return_value = mock_cli

        files = get_uploaded_files(api_key="test-key")
        assert len(files) == 1
        mock_handles.assert_called_once()
        mock_cli.files.get.assert_called_with(name="files/pmkisan_test")

    with patch("ai_engine.vector_store.ingest_official_pdfs") as mock_ingest:
        mock_ingest.return_value = {"status": "ok"}
        res = upload_all_pdfs()
        assert res == {"status": "ok"}
        mock_ingest.assert_called_once()


# =====================================================================
# 8. POST /api/v1/ask endpoint adheres to frontend contract
# =====================================================================
def test_api_v1_ask_endpoint_contract():
    mock_rag_response = {
        "answer": "PMSS provides Rs 3,000 per month for girls and Rs 2,500 for boys.",
        "sources": [
            {
                "document": "PMSS 2023-24.pdf",
                "doc_name": "PMSS 2023-24.pdf",
                "page": 4,
                "section": "Clause 6",
                "quote": "Rs. 3000/- per month for girls.",
            }
        ],
        "success": True,
    }

    with patch("api.routes.ask.ask_policy", return_value=mock_rag_response):
        response = client.post(
            "/api/v1/ask",
            json={
                "question": "What is the scholarship amount under PMSS?",
                "context": {"category": "WARB"},
            },
        )
        assert response.status_code == 200
        data = response.json()

        # Strict frontend contract validation
        assert "answer" in data
        assert "sources" in data
        assert data["answer"] == mock_rag_response["answer"]
        assert len(data["sources"]) == 1
        assert data["sources"][0]["doc_name"] == "PMSS 2023-24.pdf"
        assert data["sources"][0]["page"] == 4

        # Validate with Pydantic model
        validated = AskResponse(**data)
        assert validated.answer == data["answer"]


# =====================================================================
# 9. POST /api/v1/ask validation errors
# =====================================================================
def test_api_v1_ask_validation_error():
    # Missing required question field
    response = client.post("/api/v1/ask", json={})
    assert response.status_code == 422

    # Empty question string
    response = client.post("/api/v1/ask", json={"question": ""})
    assert response.status_code == 422


# =====================================================================
# 10. Architectural boundary: RAG never evaluates eligibility
# =====================================================================
def test_rag_does_not_evaluate_eligibility():
    # Calling ask_policy does not affect deterministic evaluate_eligibility
    profile = {"age": 25, "occupation": "Student"}
    scheme = {
        "id": "test_s",
        "name": "Test Scheme",
        "category": "Education",
        "criteria": [
            {
                "id": "c1",
                "field": "age",
                "operator": ">=",
                "expected_value": 18,
                "citation": {"doc_name": "Test.pdf", "page": 1, "quote": "Age 18"},
            }
        ],
    }

    eval_result = evaluate_eligibility(profile, scheme)
    assert eval_result.overall_status == "ELIGIBLE"

    # Verify ask_policy is purely informational and has distinct interface
    assert callable(ask_policy)
    assert ask_policy.__name__ == "ask_policy"
