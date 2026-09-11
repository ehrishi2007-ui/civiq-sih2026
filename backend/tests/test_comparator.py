"""
Unit and Integration Tests for CiviQ M7 - Policy Comparator Engine.

Validates:
1. Correct PMSS versions are 2023-24 and 2026-27.
2. Dev1's incorrect version labels (2022-23 / 2024-25) are NOT returned.
3. No unverified policy difference is presented as factual (changes == [] for unverified 2026-27).
4. Grounded 2023-24 citation is preserved correctly.
5. Missing/unverified 2026-27 evidence handled conservatively (status == UNVERIFIED_NEW_VERSION).
6. Comparator does not replace or duplicate evaluator eligibility decisions.
7. POST /api/v1/comparator endpoint exists and returns HTTP 200 with valid schema.
8. Request validation works (supports empty body {}, specific scheme_id, and user_profile).
9. Preserves backward-compatibility keys (diff_matrix, version_old, version_new).
"""

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.schemas import ComparatorRequest, ComparatorResponse
from ai_engine.comparator import compare_policy_versions
from ai_engine.evaluator import evaluate_eligibility

client = TestClient(app)


# =====================================================================
# 1. Correct PMSS versions are 2023-24 and 2026-27
# =====================================================================
def test_correct_pmss_versions_used():
    res = compare_policy_versions(scheme_id="pm_scholarship_warb")
    assert res["old_version"] == "2023-24"
    assert res["new_version"] == "2026-27"


# =====================================================================
# 2. Dev1's incorrect version labels (2022-23 / 2024-25) are NOT returned
# =====================================================================
def test_dev1_incorrect_version_labels_rejected():
    res = compare_policy_versions(scheme_id="pm_scholarship_warb")
    assert res["old_version"] != "2022-23"
    assert res["new_version"] != "2024-25"
    assert res["version_old"] != "2022-23"
    assert res["version_new"] != "2024-25"


# =====================================================================
# 3. No unverified policy difference is presented as factual (unverified fallback)
# =====================================================================
def test_no_unverified_policy_difference_fabricated():
    # When scheme has no verified policy_diff, changes must be empty
    res = compare_policy_versions(scheme_id="pmegp")
    assert res["verified"] is False
    assert res["changes"] == []
    assert res["diff_matrix"] == []


# =====================================================================
# 4. Grounded 2023-24 citation is preserved correctly
# =====================================================================
def test_grounded_2023_24_citation_preserved():
    res = compare_policy_versions(scheme_id="pm_scholarship_warb")
    assert len(res["sources"]) >= 1
    src = res["sources"][0]
    assert src["doc_name"] == "PMSS 2023-24.pdf"
    assert src["page"] == 4
    assert "Rs. 3000/- per month for girls" in src["quote"]


# =====================================================================
# 5. Missing/unverified 2026-27 evidence handled conservatively
# =====================================================================
def test_unverified_2026_27_status_and_message():
    res = compare_policy_versions(scheme_id="pmegp")
    assert res["status"] == "UNVERIFIED_NEW_VERSION"
    assert "pending OCR/multimodal verification" in res["message"]
    assert "PMSS 2026-27.pdf is a scanned image document" in res["message"]


# =====================================================================
# 6. Evaluator integration: uses evaluator without replacing it
# =====================================================================
def test_evaluator_integration_without_replacement():
    profile_student = {
        "age": 20,
        "occupation": "Student",
        "marks_percentage": 75.0,
    }
    # Deterministic evaluator remains authoritative
    res = compare_policy_versions(
        user_profile=profile_student,
        scheme_id="pm_scholarship_warb",
    )
    # The personalized impact explanation uses the deterministic evaluator output
    assert "ELIGIBLE" in res["personalized_impact"]
    assert res["impact"] is not None
    assert res["impact"]["direction"] == "positive"


# =====================================================================
# 7. POST /api/v1/comparator endpoint exists and returns HTTP 200
# =====================================================================
def test_api_v1_comparator_endpoint():
    response = client.post(
        "/api/v1/comparator",
        json={"scheme_id": "pm_scholarship_warb"},
    )
    assert response.status_code == 200
    data = response.json()

    assert data["scheme_id"] == "pm_scholarship_warb"
    assert data["old_version"] == "2023-24"
    assert data["new_version"] == "2026-27"
    assert data["verified"] is True
    assert data["status"] == "VERIFIED"
    assert len(data["changes"]) == 3
    assert len(data["sources"]) >= 1
    assert data["sources"][0]["doc_name"] == "PMSS 2023-24.pdf"

    # Schema validation
    validated = ComparatorResponse(**data)
    assert validated.scheme_id == "pm_scholarship_warb"
    assert validated.impact is not None


# =====================================================================
# 8. Request validation: supports empty body and user profile
# =====================================================================
def test_api_v1_comparator_empty_body_and_profile():
    # Empty body defaults to primary MVP comparison (PMSS)
    res_default = client.post("/api/v1/comparator", json={})
    assert res_default.status_code == 200
    assert res_default.json()["scheme_id"] == "pm_scholarship_warb"

    # With user profile
    res_profile = client.post(
        "/api/v1/comparator",
        json={
            "scheme_id": "pm_scholarship_warb",
            "user_profile": {"age": 21, "occupation": "Student", "marks_percentage": 85},
        },
    )
    assert res_profile.status_code == 200
    assert "ELIGIBLE" in res_profile.json()["personalized_impact"]


# =====================================================================
# 9. Backward-compatibility keys preserved
# =====================================================================
def test_backward_compatibility_keys_preserved():
    res = compare_policy_versions(scheme_id="pm_scholarship_warb")
    assert "version_old" in res
    assert "version_new" in res
    assert "diff_matrix" in res
    assert "personalized_impact" in res
    assert res["version_old"] == "2023-24"
    assert res["version_new"] == "2026-27"
