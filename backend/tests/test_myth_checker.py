"""
Unit and Integration Tests for CiviQ M6 - Curated Myth Buster & Misinformation Checker.

Validates:
1. Known Dev1 myth matches correctly ("Modi 50000 cash to farmers").
2. "FAKE" is mapped to "FALSE" in accordance with frontend contract.
3. Unknown claim returns "UNVERIFIED" with helpful advisory.
4. Empty / whitespace claims return controlled response / validation error.
5. Structured source citations conform to frontend contract ({document, doc_name, page, section, quote}).
6. No fabricated page numbers or citations for ungrounded claims.
7. Text normalization handles casing, punctuation, commas, and currency symbols (₹, Rs., etc.).
8. POST /api/v1/myths/check endpoint returns HTTP 200 adhering strictly to frontend contract.
9. POST /api/v1/myths/check rejects empty/missing payload with HTTP 422.
10. Architectural boundary: Myth Buster never evaluates citizen eligibility.
"""

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.schemas import MythCheckRequest, MythCheckResponse
from ai_engine.myth_checker import check_myth, load_myths, map_verdict, normalize_query
from ai_engine.evaluator import evaluate_eligibility

client = TestClient(app)


# =====================================================================
# 1. Known Dev1 myth matches correctly
# =====================================================================
def test_known_dev1_myth_matches():
    res = check_myth("Modi giving 50000 to all farmers")
    assert res["verdict"] == "FALSE"
    assert "PM-KISAN" in res["real_scheme"]
    assert "6,000" in res["explanation"]
    assert len(res["sources"]) == 1
    assert res["sources"][0]["doc_name"] == "PM-KISAN.pdf"
    assert res["sources"][0]["page"] == 2


# =====================================================================
# 2. "FAKE" verdict is exposed as "FALSE" to the frontend
# =====================================================================
def test_verdict_mapping_fake_to_false():
    assert map_verdict("FAKE") == "FALSE"
    assert map_verdict("fake") == "FALSE"
    assert map_verdict("FALSE") == "FALSE"
    assert map_verdict("TRUE") == "TRUE"
    assert map_verdict("PARTIALLY TRUE") == "PARTIALLY TRUE"
    assert map_verdict("unknown_val") == "UNVERIFIED"
    assert map_verdict(None) == "UNVERIFIED"


# =====================================================================
# 3. Unknown claim returns "UNVERIFIED"
# =====================================================================
def test_unknown_claim_returns_unverified():
    res = check_myth("Random alien subsidy announced on mars")
    assert res["verdict"] == "UNVERIFIED"
    assert "not registered in our verified fact-check database" in res["explanation"]
    assert res["sources"] == []


# =====================================================================
# 4. Empty and whitespace claims return controlled response
# =====================================================================
def test_empty_claim_handling():
    res_empty = check_myth("")
    assert res_empty["verdict"] == "UNVERIFIED"
    assert "Please provide a valid claim" in res_empty["explanation"]

    res_spaces = check_myth("     ")
    assert res_spaces["verdict"] == "UNVERIFIED"
    assert "Please provide a valid claim" in res_spaces["explanation"]


# =====================================================================
# 5. Source objects have correct structured shape
# =====================================================================
def test_source_objects_structured_shape():
    res = check_myth("PM 50000 cash scheme")
    assert len(res["sources"]) >= 1
    src = res["sources"][0]
    assert "document" in src
    assert "doc_name" in src
    assert "page" in src
    assert "section" in src
    assert "quote" in src
    assert src["document"] == "PM-KISAN.pdf"
    assert src["page"] == 2
    assert isinstance(src["quote"], str) and len(src["quote"]) > 0


# =====================================================================
# 6. No fabricated page numbers for ungrounded claims
# =====================================================================
def test_no_fabricated_page_numbers_for_ungrounded():
    # Myth 2: Free laptop scheme (not supported by approved PDF corpus)
    res_laptop = check_myth("Free laptop scheme 2026 apply now")
    assert res_laptop["verdict"] == "UNVERIFIED"
    # Must NOT fabricate a fake page number or fake PDF citation
    assert res_laptop["sources"] == []

    # Myth 3: 8000 monthly pension (operational circular does not establish citizen tiers)
    res_pension = check_myth("8000 monthly pension yojana")
    assert res_pension["verdict"] == "UNVERIFIED"
    assert res_pension["sources"] == []

    # Myth 4: 12 free cylinders (PMUY not in approved 6-PDF corpus)
    res_cylinder = check_myth("12 free cylinders scheme")
    assert res_cylinder["verdict"] == "UNVERIFIED"
    assert res_cylinder["sources"] == []

    # Myth 5: 2 lakh accident insurance (PMSBY not in approved 6-PDF corpus)
    res_insurance = check_myth("2 lakh accident insurance free whatsapp")
    assert res_insurance["verdict"] == "UNVERIFIED"
    assert res_insurance["sources"] == []


# =====================================================================
# 7. Text normalization: casing, punctuation, commas, currency symbols
# =====================================================================
def test_query_normalization():
    # Verify normalize_query helper
    assert "50000" in normalize_query("₹50,000")
    assert "rs 50000" in normalize_query("Rs. 50,000")
    assert "modi 50000" in normalize_query("MODI, 50,000!!")

    # Verify check_myth matches various permutations
    res1 = check_myth("modi 50000")
    res2 = check_myth("MODI ₹50,000 FARMERS")
    res3 = check_myth("pm-kisan gives ₹10,000 per year")
    assert res1["verdict"] == "FALSE"
    assert res2["verdict"] == "FALSE"
    assert res3["verdict"] == "FALSE"


# =====================================================================
# 8. POST /api/v1/myths/check endpoint adheres strictly to contract
# =====================================================================
def test_api_v1_myths_check_endpoint():
    response = client.post(
        "/api/v1/myths/check",
        json={"claim": "PM-KISAN gives ₹10,000 per year"},
    )
    assert response.status_code == 200
    data = response.json()

    # Exact frontend contract validation
    assert "verdict" in data
    assert "explanation" in data
    assert "sources" in data
    assert data["verdict"] == "FALSE"
    assert len(data["sources"]) == 1
    assert data["sources"][0]["doc_name"] == "PM-KISAN.pdf"
    assert data["sources"][0]["page"] == 2

    # Pydantic schema validation
    validated = MythCheckResponse(**data)
    assert validated.verdict == "FALSE"


# =====================================================================
# 9. POST /api/v1/myths/check validation errors
# =====================================================================
def test_api_v1_myths_check_validation_error():
    # Missing required 'claim' field
    res_missing = client.post("/api/v1/myths/check", json={})
    assert res_missing.status_code == 422

    # Empty string claim
    res_empty = client.post("/api/v1/myths/check", json={"claim": ""})
    assert res_empty.status_code == 422


# =====================================================================
# 10. Architectural boundary: Myth Buster never evaluates eligibility
# =====================================================================
def test_myth_buster_does_not_evaluate_eligibility():
    profile = {"age": 45, "occupation": "Farmer", "has_land": True}
    scheme = {
        "id": "pm_kisan",
        "name": "PM-KISAN",
        "category": "Agriculture",
        "criteria": [
            {
                "id": "c_land",
                "field": "has_land",
                "operator": "==",
                "expected_value": True,
                "citation": {"doc_name": "PM-KISAN.pdf", "page": 2, "quote": "owns cultivable land"},
            }
        ],
    }

    # Deterministic evaluator remains authoritative
    eval_result = evaluate_eligibility(profile, scheme)
    assert eval_result.overall_status == "ELIGIBLE"

    # Myth check is an independent service with no effect on profile or evaluator
    myth_res = check_myth("Modi giving 50000 to all farmers")
    assert myth_res["verdict"] == "FALSE"
    assert eval_result.overall_status == "ELIGIBLE"
