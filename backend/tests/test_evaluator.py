"""
Unit tests for the CiviQ Deterministic Eligibility Evaluator and Scheme Data Contract.

Validates that eligibility is determined strictly by deterministic Python logic
without AI, LLM, or fuzzy heuristics.
"""

import json
from pathlib import Path
import pytest

from ai_engine.evaluator import evaluate_eligibility, SUPPORTED_OPERATORS
from ai_engine.schemas import (
    Citation,
    Criterion,
    CriterionStatus,
    EvaluationResult,
    OverallStatus,
    Scheme,
    validate_scheme,
    validate_schemes_list,
)


def _make_scheme(criteria, scheme_id="test_scheme", scheme_name="Test Scheme"):
    """Helper to construct a scheme dictionary for testing."""
    return {
        "id": scheme_id,
        "name": scheme_name,
        "ministry": "Ministry of Social Justice",
        "short_desc": "A test scheme for unit tests",
        "benefit_summary": "Financial support",
        "application_url": "https://example.gov.in/apply",
        "closing_date": "2026-12-31",
        "version_year": 2026,
        "criteria": criteria,
    }


def _make_criterion(
    criterion_id="crit_1",
    field="age",
    operator=">=",
    expected_value=18,
    doc_name="guidelines.pdf",
    page=5,
    section="Eligibility",
    quote="Must be 18 or older.",
):
    """Helper to construct a criterion dictionary with citation."""
    return {
        "id": criterion_id,
        "field": field,
        "operator": operator,
        "expected_value": expected_value,
        "citation": {
            "doc_name": doc_name,
            "page": page,
            "section": section,
            "quote": quote,
        },
    }


# =====================================================================
# 1. == PASS
# =====================================================================
def test_operator_eq_pass():
    profile = {"occupation": "Student"}
    scheme = _make_scheme([_make_criterion(field="occupation", operator="==", expected_value="Student")])
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.ELIGIBLE.value
    assert result.passed_count == 1
    assert result.failed_count == 0
    assert result.missing_count == 0
    assert result.criteria[0].status == CriterionStatus.PASS.value
    assert result.criteria[0].user_value == "Student"


# =====================================================================
# 2. == FAIL
# =====================================================================
def test_operator_eq_fail():
    profile = {"occupation": "Engineer"}
    scheme = _make_scheme([_make_criterion(field="occupation", operator="==", expected_value="Student")])
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.NOT_ELIGIBLE.value
    assert result.passed_count == 0
    assert result.failed_count == 1
    assert result.missing_count == 0
    assert result.criteria[0].status == CriterionStatus.FAIL.value


# =====================================================================
# 3. != PASS
# =====================================================================
def test_operator_neq_pass():
    profile = {"state": "Tamil Nadu"}
    scheme = _make_scheme([_make_criterion(field="state", operator="!=", expected_value="Kerala")])
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.ELIGIBLE.value
    assert result.passed_count == 1
    assert result.criteria[0].status == CriterionStatus.PASS.value


# =====================================================================
# 4. > PASS
# =====================================================================
def test_operator_gt_pass():
    profile = {"annual_income": 300000}
    scheme = _make_scheme([_make_criterion(field="annual_income", operator=">", expected_value=200000)])
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.ELIGIBLE.value
    assert result.criteria[0].status == CriterionStatus.PASS.value


# =====================================================================
# 5. > FAIL
# =====================================================================
def test_operator_gt_fail():
    profile = {"annual_income": 150000}
    scheme = _make_scheme([_make_criterion(field="annual_income", operator=">", expected_value=200000)])
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.NOT_ELIGIBLE.value
    assert result.criteria[0].status == CriterionStatus.FAIL.value


# =====================================================================
# 6. >= PASS
# =====================================================================
def test_operator_gte_pass():
    profile = {"age": 18}
    scheme = _make_scheme([_make_criterion(field="age", operator=">=", expected_value=18)])
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.ELIGIBLE.value
    assert result.criteria[0].status == CriterionStatus.PASS.value


# =====================================================================
# 7. <= PASS
# =====================================================================
def test_operator_lte_pass():
    profile = {"annual_income": 200000}
    scheme = _make_scheme([_make_criterion(field="annual_income", operator="<=", expected_value=200000)])
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.ELIGIBLE.value
    assert result.criteria[0].status == CriterionStatus.PASS.value


# =====================================================================
# 8. < PASS
# =====================================================================
def test_operator_lt_pass():
    profile = {"age": 17}
    scheme = _make_scheme([_make_criterion(field="age", operator="<", expected_value=18)])
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.ELIGIBLE.value
    assert result.criteria[0].status == CriterionStatus.PASS.value


# =====================================================================
# 9. in PASS
# =====================================================================
def test_operator_in_pass():
    profile = {"category": "SC"}
    scheme = _make_scheme([_make_criterion(field="category", operator="in", expected_value=["SC", "ST"])])
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.ELIGIBLE.value
    assert result.criteria[0].status == CriterionStatus.PASS.value


# =====================================================================
# 10. in FAIL
# =====================================================================
def test_operator_in_fail():
    profile = {"category": "General"}
    scheme = _make_scheme([_make_criterion(field="category", operator="in", expected_value=["SC", "ST"])])
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.NOT_ELIGIBLE.value
    assert result.criteria[0].status == CriterionStatus.FAIL.value


# =====================================================================
# 11. missing profile field
# =====================================================================
def test_missing_profile_field():
    profile = {"name": "Priya Ramesh"}  # age is completely missing
    scheme = _make_scheme([_make_criterion(field="age", operator=">=", expected_value=18)])
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.INSUFFICIENT_DATA.value
    assert result.missing_count == 1
    assert result.passed_count == 0
    assert result.failed_count == 0
    assert result.criteria[0].status == CriterionStatus.MISSING_DATA.value
    assert result.criteria[0].user_value is None
    assert "missing" in result.criteria[0].reason.lower()


# =====================================================================
# 12. None profile value
# =====================================================================
def test_none_profile_value():
    profile = {"age": None}
    scheme = _make_scheme([_make_criterion(field="age", operator=">=", expected_value=18)])
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.INSUFFICIENT_DATA.value
    assert result.missing_count == 1
    assert result.passed_count == 0
    assert result.failed_count == 0
    assert result.criteria[0].status == CriterionStatus.MISSING_DATA.value
    assert "None" in result.criteria[0].reason


# =====================================================================
# 13. invalid operator
# =====================================================================
def test_invalid_operator():
    profile = {"age": 21}
    scheme = _make_scheme([_make_criterion(field="age", operator="LIKE", expected_value=21)])
    result = evaluate_eligibility(profile, scheme)

    # Fails safely: invalid operators are rejected without crashing
    assert result.overall_status == OverallStatus.NOT_ELIGIBLE.value
    assert result.failed_count == 1
    assert result.criteria[0].status == CriterionStatus.FAIL.value
    assert "Unsupported operator" in result.criteria[0].reason


# =====================================================================
# 14. multiple criteria all passing
# =====================================================================
def test_multiple_criteria_all_passing():
    profile = {
        "age": 21,
        "occupation": "Student",
        "state": "Tamil Nadu",
        "annual_income": 150000,
    }
    criteria = [
        _make_criterion("c1", "age", ">=", 18),
        _make_criterion("c2", "occupation", "==", "Student"),
        _make_criterion("c3", "state", "==", "Tamil Nadu"),
        _make_criterion("c4", "annual_income", "<=", 250000),
    ]
    scheme = _make_scheme(criteria)
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.ELIGIBLE.value
    assert result.passed_count == 4
    assert result.failed_count == 0
    assert result.missing_count == 0
    assert len(result.criteria) == 4
    assert all(c.status == CriterionStatus.PASS.value for c in result.criteria)


# =====================================================================
# 15. multiple criteria with one failure
# =====================================================================
def test_multiple_criteria_with_one_failure():
    profile = {
        "age": 21,
        "occupation": "Student",
        "state": "Kerala",  # Fails state criterion
        "annual_income": 150000,
    }
    criteria = [
        _make_criterion("c1", "age", ">=", 18),
        _make_criterion("c2", "occupation", "==", "Student"),
        _make_criterion("c3", "state", "==", "Tamil Nadu"),
        _make_criterion("c4", "annual_income", "<=", 250000),
    ]
    scheme = _make_scheme(criteria)
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.NOT_ELIGIBLE.value
    assert result.passed_count == 3
    assert result.failed_count == 1
    assert result.missing_count == 0


# =====================================================================
# 16. multiple criteria with missing data
# =====================================================================
def test_multiple_criteria_with_missing_data():
    profile = {
        "age": 21,
        "occupation": "Student",
        # state and annual_income are omitted
    }
    criteria = [
        _make_criterion("c1", "age", ">=", 18),
        _make_criterion("c2", "occupation", "==", "Student"),
        _make_criterion("c3", "state", "==", "Tamil Nadu"),
        _make_criterion("c4", "annual_income", "<=", 250000),
    ]
    scheme = _make_scheme(criteria)
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.INSUFFICIENT_DATA.value
    assert result.passed_count == 2
    assert result.failed_count == 0
    assert result.missing_count == 2


# =====================================================================
# 17. citation preservation
# =====================================================================
def test_citation_preservation():
    profile = {"age": 25}
    citation_data = {
        "doc_name": "Official_Guidelines_2026.pdf",
        "page": 14,
        "section": "Clause 3.2: Eligibility Requirements",
        "quote": "Applicant must have completed 18 years of age at the time of filing.",
    }
    criterion = _make_criterion(
        criterion_id="age_rule_v1",
        field="age",
        operator=">=",
        expected_value=18,
        doc_name=citation_data["doc_name"],
        page=citation_data["page"],
        section=citation_data["section"],
        quote=citation_data["quote"],
    )
    scheme = _make_scheme([criterion])
    result = evaluate_eligibility(profile, scheme)

    crit_res = result.criteria[0]
    assert crit_res.criterion_id == "age_rule_v1"
    assert crit_res.citation == citation_data
    assert crit_res.citation["doc_name"] == "Official_Guidelines_2026.pdf"
    assert crit_res.citation["page"] == 14
    assert crit_res.citation["section"] == "Clause 3.2: Eligibility Requirements"
    assert crit_res.citation["quote"] == "Applicant must have completed 18 years of age at the time of filing."


# =====================================================================
# 18. numeric comparison
# =====================================================================
def test_numeric_comparison():
    # Floating point numbers and integers
    profile = {"land_acres": 2.5, "family_members": 4}
    criteria = [
        _make_criterion("c_land", "land_acres", "<=", 5.0),
        _make_criterion("c_members", "family_members", ">", 2),
    ]
    scheme = _make_scheme(criteria)
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.ELIGIBLE.value
    assert result.passed_count == 2


# =====================================================================
# 19. string comparison
# =====================================================================
def test_string_comparison():
    profile = {"gender": "female", "district": "Chennai"}
    criteria = [
        _make_criterion("c_gender", "gender", "==", "female"),
        _make_criterion("c_district", "district", "!=", "Madurai"),
    ]
    scheme = _make_scheme(criteria)
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.ELIGIBLE.value
    assert result.passed_count == 2


# =====================================================================
# 20. empty criteria handling
# =====================================================================
def test_empty_criteria_handling():
    profile = {"name": "Priya Ramesh"}
    scheme = _make_scheme([])
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.ELIGIBLE.value
    assert result.passed_count == 0
    assert result.failed_count == 0
    assert result.missing_count == 0
    assert len(result.criteria) == 0


# =====================================================================
# Additional Robustness Tests: Type Safety, Fail-Safe, Pydantic Schema
# =====================================================================
def test_type_mismatch_numeric_fail_safe():
    """Ensure non-numeric string given for numeric comparison fails safely without throwing."""
    profile = {"annual_income": "two lakhs"}  # Invalid type: str instead of int
    scheme = _make_scheme([_make_criterion(field="annual_income", operator="<=", expected_value=200000)])
    result = evaluate_eligibility(profile, scheme)

    # Missing/invalid required profile data produces INSUFFICIENT_DATA
    assert result.overall_status == OverallStatus.INSUFFICIENT_DATA.value
    assert result.missing_count == 1
    assert result.criteria[0].status == CriterionStatus.MISSING_DATA.value
    assert "Incompatible types" in result.criteria[0].reason


def test_membership_in_with_user_list():
    """Test membership when profile contains a list of documents."""
    profile = {"documents": ["Aadhaar", "Income Certificate", "Land Record"]}
    scheme = _make_scheme([_make_criterion(field="documents", operator="in", expected_value="Aadhaar")])
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.ELIGIBLE.value
    assert result.criteria[0].status == CriterionStatus.PASS.value


def test_failure_precedence_over_missing_data():
    """If a criterion has failed, overall_status is NOT_ELIGIBLE even if another field is missing."""
    profile = {
        "age": 15,  # Fails age >= 18
        # annual_income is missing
    }
    criteria = [
        _make_criterion("c1", "age", ">=", 18),
        _make_criterion("c2", "annual_income", "<=", 200000),
    ]
    scheme = _make_scheme(criteria)
    result = evaluate_eligibility(profile, scheme)

    assert result.overall_status == OverallStatus.NOT_ELIGIBLE.value
    assert result.failed_count == 1
    assert result.missing_count == 1
    assert result.passed_count == 0


def test_pydantic_scheme_validation():
    """Validates that a Scheme model parses properly from a dict."""
    scheme_dict = _make_scheme([_make_criterion()])
    scheme_obj = validate_scheme(scheme_dict)

    assert isinstance(scheme_obj, Scheme)
    assert scheme_obj.id == "test_scheme"
    assert len(scheme_obj.criteria) == 1
    assert isinstance(scheme_obj.criteria[0].citation, Citation)

    # Test passing Scheme instance directly into evaluator
    profile = {"age": 21}
    result = evaluate_eligibility(profile, scheme_obj)
    assert result.overall_status == OverallStatus.ELIGIBLE.value


def test_canonical_schemes_extracted_file_contract():
    """Validates that data/schemes_extracted.json is present and valid against schema."""
    json_path = Path(__file__).resolve().parent.parent.parent / "data" / "schemes_extracted.json"
    assert json_path.exists(), f"Missing canonical file: {json_path}"

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) >= 3  # Verified canonical MVP schemes
    validated = validate_schemes_list(data)
    assert len(validated) == len(data)


def test_result_dict_and_attr_access():
    """Ensures EvaluationResult supports both dot notation and dictionary-style access."""
    profile = {"age": 20}
    scheme = _make_scheme([_make_criterion(field="age", operator=">=", expected_value=18)])
    result = evaluate_eligibility(profile, scheme)

    # Dot notation
    assert result.overall_status == "ELIGIBLE"
    assert result.passed_count == 1

    # Dictionary access
    assert result["overall_status"] == "ELIGIBLE"
    assert result["passed_count"] == 1
    assert result.get("failed_count") == 0

    # CriterionResult access
    assert result.criteria[0]["status"] == "PASS"
    assert result.criteria[0].get("criterion_id") == "crit_1"
