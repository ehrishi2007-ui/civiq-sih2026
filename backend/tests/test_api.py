"""
Integration tests for CiviQ FastAPI Foundation and Match Routes.
Validates HTTP contracts, schema enforcement, evaluator integration, and fail-safe handling.
"""

import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "synthetic_scheme.json"


def _load_synthetic_fixture():
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _make_valid_profile():
    return {
        "full_name": "Ananya Sharma",
        "age": 20,
        "gender": "female",
        "category": "General",
        "annual_income": 120000.0,
        "state": "Karnataka",
        "district": "Bengaluru",
        "is_rural": False,
        "occupation": "Student",
        "education": "Undergraduate",
        "has_land": False,
        "land_acres": 0.0,
        "has_bpl_card": False,
        "disability": False,
        "minority": False,
        "ration_card_type": "None",
        "documents": ["Aadhaar", "Student ID"],
    }


# =====================================================================
# 1. GET /health
# =====================================================================
def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


# =====================================================================
# 2. valid profile (POST /api/v1/profile)
# =====================================================================
def test_valid_profile():
    profile = _make_valid_profile()
    response = client.post("/api/v1/profile", json=profile)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Ananya Sharma"
    assert data["age"] == 20
    assert data["occupation"] == "Student"
    assert data["status"] == "success"


# =====================================================================
# 3. invalid profile (POST /api/v1/profile)
# =====================================================================
def test_invalid_profile():
    # Missing required fields like 'full_name' and negative age
    invalid_profile = {
        "age": -5,
        "occupation": "Student",
    }
    response = client.post("/api/v1/profile", json=invalid_profile)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


# =====================================================================
# 4. successful match (POST /api/v1/match)
# =====================================================================
def test_successful_match():
    profile = _make_valid_profile()
    synthetic_scheme = _load_synthetic_fixture()

    payload = {
        "profile": profile,
        "schemes": [synthetic_scheme],
    }
    response = client.post("/api/v1/match", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["total_evaluated"] == 1
    assert data["eligible_count"] == 1
    match = data["matches"][0]
    assert match["scheme_id"] == "synthetic_demo_scheme"
    assert match["overall_status"] == "ELIGIBLE"
    assert match["eligible"] is True
    assert match["passed_count"] == 3
    assert match["failed_count"] == 0
    assert match["missing_count"] == 0


# =====================================================================
# 5. failed criterion (POST /api/v1/match)
# =====================================================================
def test_failed_criterion():
    profile = _make_valid_profile()
    profile["occupation"] = "Engineer"  # Fails occupation == "Student"
    synthetic_scheme = _load_synthetic_fixture()

    payload = {
        "profile": profile,
        "schemes": [synthetic_scheme],
    }
    response = client.post("/api/v1/match", json=payload)
    assert response.status_code == 200
    data = response.json()

    match = data["matches"][0]
    assert match["overall_status"] == "NOT_ELIGIBLE"
    assert match["eligible"] is False
    assert match["failed_count"] == 1
    assert match["passed_count"] == 2

    # Find the occupation criterion
    occ_crit = next(c for c in match["criteria"] if c["field"] == "occupation")
    assert occ_crit["status"] == "FAIL"
    assert occ_crit["pass_status"] is False


# =====================================================================
# 6. insufficient profile data (POST /api/v1/match)
# =====================================================================
def test_insufficient_profile_data():
    profile = _make_valid_profile()
    # Profile lacks the field evaluated by a criterion
    custom_scheme = _load_synthetic_fixture()
    custom_scheme["criteria"].append({
        "id": "crit_caste_cert",
        "field": "caste_certificate_number",  # Not in profile
        "operator": "!=",
        "expected_value": "",
        "citation": {
            "doc_name": "Guidelines.pdf",
            "page": 1,
            "section": "Documents",
            "quote": "Caste certificate required.",
        },
    })

    payload = {
        "profile": profile,
        "schemes": [custom_scheme],
    }
    response = client.post("/api/v1/match", json=payload)
    assert response.status_code == 200
    data = response.json()

    match = data["matches"][0]
    assert match["overall_status"] == "INSUFFICIENT_DATA"
    assert match["eligible"] is False
    assert match["missing_count"] == 1


# =====================================================================
# 7. citation preservation (POST /api/v1/match)
# =====================================================================
def test_citation_preservation():
    profile = _make_valid_profile()
    synthetic_scheme = _load_synthetic_fixture()

    payload = {
        "profile": profile,
        "schemes": [synthetic_scheme],
    }
    response = client.post("/api/v1/match", json=payload)
    assert response.status_code == 200
    data = response.json()

    match = data["matches"][0]
    assert len(match["citations"]) == 3
    # Check first criterion citation
    first_crit = match["criteria"][0]
    assert first_crit["citation"]["doc_name"] == "Synthetic_Guidelines_2026.pdf"
    assert first_crit["citation"]["page"] == 2
    assert first_crit["citation"]["section"] == "Section 1: Age Eligibility"
    assert "at least 18 years" in first_crit["citation"]["quote"]


# =====================================================================
# 8. malformed request (POST /api/v1/match)
# =====================================================================
def test_malformed_request():
    # Pass string instead of dict
    response = client.post(
        "/api/v1/match",
        content="This is not JSON",
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400
    assert "Malformed JSON" in response.json()["detail"]


# =====================================================================
# 9. unsupported operator (POST /api/v1/match)
# =====================================================================
def test_unsupported_operator():
    profile = _make_valid_profile()
    bad_scheme = {
        "id": "bad_op_scheme",
        "name": "Bad Operator Scheme",
        "version_year": 2026,
        "criteria": [
            {
                "id": "crit_bad",
                "field": "age",
                "operator": "REGEX_MATCH",  # Unsupported operator
                "expected_value": "^18$",
                "citation": {
                    "doc_name": "doc.pdf",
                    "page": 1,
                    "section": "Sec",
                    "quote": "Quote",
                },
            }
        ],
    }

    payload = {
        "profile": profile,
        "schemes": [bad_scheme],
    }
    response = client.post("/api/v1/match", json=payload)
    assert response.status_code == 200
    data = response.json()

    match = data["matches"][0]
    # Fails safely without 500 error
    assert match["overall_status"] == "NOT_ELIGIBLE"
    assert match["failed_count"] == 1
    assert "Unsupported operator" in match["criteria"][0]["reason"]


# =====================================================================
# 10. multiple criteria (POST /api/v1/match)
# =====================================================================
def test_multiple_criteria():
    profile = _make_valid_profile()
    synthetic_scheme = _load_synthetic_fixture()

    payload = {
        "profile": profile,
        "schemes": [synthetic_scheme],
    }
    response = client.post("/api/v1/match", json=payload)
    assert response.status_code == 200
    data = response.json()

    match = data["matches"][0]
    assert len(match["criteria"]) == 3
    assert match["passed_count"] == 3
    assert match["failed_count"] == 0
    assert match["missing_count"] == 0
    assert match["score"] == 1.0


# =====================================================================
# 11. direct profile payload compatibility (frontend style)
# =====================================================================
def test_direct_profile_payload():
    profile = _make_valid_profile()
    response = client.post("/api/v1/match", json=profile)
    assert response.status_code == 200
    data = response.json()
    # Evaluates against canonical data/schemes_extracted.json (currently empty)
    assert data["total_evaluated"] == 0
    assert data["matches"] == []
