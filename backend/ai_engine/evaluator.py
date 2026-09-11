"""
CiviQ Backend - Deterministic Eligibility Evaluator.

The evaluator is the sole authority for scheme eligibility in CiviQ.
Eligibility decisions are computed exclusively through deterministic Python logic;
no AI, LLM, or fuzzy heuristics are permitted to make eligibility determinations.
"""

from typing import Any, Dict, List, Union

from .schemas import (
    CriterionResult,
    CriterionStatus,
    EvaluationResult,
    OverallStatus,
    Scheme,
    validate_scheme,
)

SUPPORTED_OPERATORS = {"==", "!=", ">", ">=", "<", "<=", "in"}


def _is_numeric(val: Any) -> bool:
    """Checks if a value is numeric (int or float) and not boolean."""
    return isinstance(val, (int, float)) and not isinstance(val, bool)


def _evaluate_criterion(
    profile: Union[Dict[str, Any], Any],
    criterion_data: Union[Dict[str, Any], Any],
) -> CriterionResult:
    """
    Evaluates a single scheme criterion against a user profile deterministically.
    Preserves provenance (citation) and criterion identification.
    """
    # 1. Resolve criterion properties
    if isinstance(criterion_data, dict):
        criterion_id = str(criterion_data.get("id", "unknown_criterion"))
        field = criterion_data.get("field")
        operator = criterion_data.get("operator")
        expected_val = criterion_data.get("expected_value")
        citation = criterion_data.get("citation", {})
        if hasattr(citation, "model_dump"):
            citation = citation.model_dump()
    else:
        criterion_id = getattr(criterion_data, "id", "unknown_criterion")
        field = getattr(criterion_data, "field", None)
        operator = getattr(criterion_data, "operator", None)
        expected_val = getattr(criterion_data, "expected_value", None)
        citation_obj = getattr(criterion_data, "citation", {})
        citation = citation_obj.model_dump() if hasattr(citation_obj, "model_dump") else dict(citation_obj)

    citation_dict = dict(citation) if isinstance(citation, dict) else {}

    # 2. Check for criterion structure validity
    if not field or not operator:
        return CriterionResult(
            criterion_id=criterion_id,
            status=CriterionStatus.FAIL.value,
            user_value=None,
            expected_value=expected_val,
            operator=str(operator) if operator else "",
            citation=citation_dict,
            reason="Invalid criterion structure: 'field' or 'operator' missing",
        )

    # 3. Check operator support
    if operator not in SUPPORTED_OPERATORS:
        return CriterionResult(
            criterion_id=criterion_id,
            status=CriterionStatus.FAIL.value,
            user_value=None,
            expected_value=expected_val,
            operator=str(operator),
            citation=citation_dict,
            reason=f"Unsupported operator '{operator}'. Supported: {sorted(list(SUPPORTED_OPERATORS))}",
        )

    # 4. Resolve profile field value
    if isinstance(profile, dict):
        has_field = field in profile
        user_val = profile.get(field)
    else:
        has_field = hasattr(profile, field)
        user_val = getattr(profile, field, None)

    # 5. Handle missing profile field
    if not has_field:
        return CriterionResult(
            criterion_id=criterion_id,
            status=CriterionStatus.MISSING_DATA.value,
            user_value=None,
            expected_value=expected_val,
            operator=operator,
            citation=citation_dict,
            reason=f"Required profile field '{field}' is missing from user profile",
        )

    # 6. Handle None profile value
    if user_val is None:
        return CriterionResult(
            criterion_id=criterion_id,
            status=CriterionStatus.MISSING_DATA.value,
            user_value=None,
            expected_value=expected_val,
            operator=operator,
            citation=citation_dict,
            reason=f"Required profile field '{field}' is None",
        )

    # 7. Deterministic evaluation by operator with type safety
    try:
        if operator == "==":
            passed = (user_val == expected_val)
            return CriterionResult(
                criterion_id=criterion_id,
                status=CriterionStatus.PASS.value if passed else CriterionStatus.FAIL.value,
                user_value=user_val,
                expected_value=expected_val,
                operator=operator,
                citation=citation_dict,
            )

        elif operator == "!=":
            passed = (user_val != expected_val)
            return CriterionResult(
                criterion_id=criterion_id,
                status=CriterionStatus.PASS.value if passed else CriterionStatus.FAIL.value,
                user_value=user_val,
                expected_value=expected_val,
                operator=operator,
                citation=citation_dict,
            )

        elif operator in {">", ">=", "<", "<="}:
            # Ensure type compatibility for ordered comparisons
            user_is_num = _is_numeric(user_val)
            exp_is_num = _is_numeric(expected_val)

            if user_is_num and exp_is_num:
                if operator == ">":
                    passed = user_val > expected_val
                elif operator == ">=":
                    passed = user_val >= expected_val
                elif operator == "<":
                    passed = user_val < expected_val
                elif operator == "<=":
                    passed = user_val <= expected_val
            elif isinstance(user_val, str) and isinstance(expected_val, str):
                if operator == ">":
                    passed = user_val > expected_val
                elif operator == ">=":
                    passed = user_val >= expected_val
                elif operator == "<":
                    passed = user_val < expected_val
                elif operator == "<=":
                    passed = user_val <= expected_val
            else:
                # Incompatible comparison types: fail safely as invalid/missing data without guessing
                return CriterionResult(
                    criterion_id=criterion_id,
                    status=CriterionStatus.MISSING_DATA.value,
                    user_value=user_val,
                    expected_value=expected_val,
                    operator=operator,
                    citation=citation_dict,
                    reason=f"Incompatible types for comparison '{operator}': {type(user_val).__name__} vs {type(expected_val).__name__}",
                )

            return CriterionResult(
                criterion_id=criterion_id,
                status=CriterionStatus.PASS.value if passed else CriterionStatus.FAIL.value,
                user_value=user_val,
                expected_value=expected_val,
                operator=operator,
                citation=citation_dict,
            )

        elif operator == "in":
            if isinstance(expected_val, (list, tuple, set, dict)):
                passed = user_val in expected_val
            elif isinstance(user_val, (list, tuple, set, dict)):
                passed = expected_val in user_val
            elif isinstance(expected_val, str) and isinstance(user_val, str):
                passed = user_val in expected_val
            else:
                return CriterionResult(
                    criterion_id=criterion_id,
                    status=CriterionStatus.FAIL.value,
                    user_value=user_val,
                    expected_value=expected_val,
                    operator=operator,
                    citation=citation_dict,
                    reason=f"Operator 'in' requires a collection or string, got {type(expected_val).__name__} and {type(user_val).__name__}",
                )

            return CriterionResult(
                criterion_id=criterion_id,
                status=CriterionStatus.PASS.value if passed else CriterionStatus.FAIL.value,
                user_value=user_val,
                expected_value=expected_val,
                operator=operator,
                citation=citation_dict,
            )

    except Exception as e:
        # Fallback safe failure
        return CriterionResult(
            criterion_id=criterion_id,
            status=CriterionStatus.FAIL.value,
            user_value=user_val,
            expected_value=expected_val,
            operator=operator,
            citation=citation_dict,
            reason=f"Evaluation error: {str(e)}",
        )

    return CriterionResult(
        criterion_id=criterion_id,
        status=CriterionStatus.FAIL.value,
        user_value=user_val,
        expected_value=expected_val,
        operator=operator,
        citation=citation_dict,
        reason="Unreachable evaluation branch",
    )


def evaluate_eligibility(
    profile: Union[Dict[str, Any], Any],
    scheme: Union[Dict[str, Any], Scheme],
) -> EvaluationResult:
    """
    Evaluates a profile against a scheme deterministically.

    Overall Status Rules:
    - Any criterion FAIL -> NOT_ELIGIBLE
    - Missing/invalid required profile data -> INSUFFICIENT_DATA
    - All criteria PASS -> ELIGIBLE
    """
    # Extract scheme identity and criteria
    if isinstance(scheme, Scheme):
        scheme_id = scheme.id
        criteria_list = scheme.criteria
    elif isinstance(scheme, dict):
        scheme_id = str(scheme.get("id", scheme.get("scheme_id", "unknown_scheme")))
        criteria_list = scheme.get("criteria", [])
    else:
        validated = validate_scheme(scheme)
        scheme_id = validated.id
        criteria_list = validated.criteria

    results: List[CriterionResult] = []

    for crit in criteria_list:
        res = _evaluate_criterion(profile, crit)
        results.append(res)

    passed_count = sum(1 for r in results if r.status == CriterionStatus.PASS.value)
    failed_count = sum(1 for r in results if r.status == CriterionStatus.FAIL.value)
    missing_count = sum(1 for r in results if r.status == CriterionStatus.MISSING_DATA.value)

    # Derive overall status deterministically
    if failed_count > 0:
        overall_status = OverallStatus.NOT_ELIGIBLE.value
    elif missing_count > 0:
        overall_status = OverallStatus.INSUFFICIENT_DATA.value
    else:
        overall_status = OverallStatus.ELIGIBLE.value

    return EvaluationResult(
        scheme_id=scheme_id,
        overall_status=overall_status,
        criteria=results,
        passed_count=passed_count,
        failed_count=failed_count,
        missing_count=missing_count,
    )
