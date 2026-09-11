"""
CiviQ Deterministic Scheme Eligibility Evaluator.
Sole authority for scheme qualification: zero LLM hallucination in eligibility logic.
"""

from typing import Any, Dict, List, Optional, Set, Union

try:
    from backend.ai_engine.schemas import (
        Citation,
        Criterion,
        CriterionResult,
        CriterionStatus,
        EvaluationResult,
        OverallStatus,
        Scheme,
        validate_scheme,
    )
except ModuleNotFoundError:
    from ai_engine.schemas import (
        Citation,
        Criterion,
        CriterionResult,
        CriterionStatus,
        EvaluationResult,
        OverallStatus,
        Scheme,
        validate_scheme,
    )

SUPPORTED_OPERATORS: Set[str] = {"==", "!=", ">", ">=", "<", "<=", "in"}


def _is_numeric(val: Any) -> bool:
    """Checks if a value is numeric (int or float, excluding booleans)."""
    return isinstance(val, (int, float)) and not isinstance(val, bool)


def _to_numeric(val: Any) -> Optional[float]:
    """Attempts to convert string representation of numbers to float."""
    if _is_numeric(val):
        return float(val)
    if isinstance(val, str):
        try:
            return float(val.replace(",", "").strip())
        except ValueError:
            return None
    return None


def evaluate_criterion(
    profile: Union[Dict[str, Any], Any],
    criterion: Union[Dict[str, Any], Criterion],
) -> CriterionResult:
    """
    Evaluates a single criterion rule against a citizen's profile.
    Deterministic Python evaluation — zero LLM hallucination.
    """
    # 1. Normalize criterion inputs
    if isinstance(criterion, Criterion):
        criterion_id = criterion.id
        field = criterion.field
        operator = criterion.operator
        expected_val = criterion.expected_value
        citation_dict = criterion.citation.model_dump() if criterion.citation else {}
        label = criterion.label or field
    elif isinstance(criterion, dict):
        criterion_id = str(criterion.get("id", f"crit_{criterion.get('field', 'unknown')}"))
        field = str(criterion.get("field", ""))
        operator = str(criterion.get("operator", "=="))
        expected_val = criterion.get("expected_value")
        raw_cit = criterion.get("citation", {})
        citation_dict = raw_cit if isinstance(raw_cit, dict) else (raw_cit.model_dump() if hasattr(raw_cit, "model_dump") else {})
        label = criterion.get("label", field)
    else:
        return CriterionResult(
            criterion_id="malformed_criterion",
            status=CriterionStatus.FAIL.value,
            user_value=None,
            expected_value=None,
            operator="==",
            citation={},
            reason="Criterion must be a dictionary or Criterion model",
        )

    # 2. Check operator support
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

    # 3. Resolve profile field value
    if isinstance(profile, dict):
        has_field = field in profile
        user_val = profile.get(field)
    else:
        has_field = hasattr(profile, field)
        user_val = getattr(profile, field, None)

    # 4. Handle missing or None profile field
    if not has_field or user_val is None:
        return CriterionResult(
            criterion_id=criterion_id,
            status=CriterionStatus.MISSING_DATA.value,
            user_value=None,
            expected_value=expected_val,
            operator=operator,
            citation=citation_dict,
            reason=f"Required profile field '{field}' is missing or None",
        )

    # 5. Deterministic evaluation by operator with type safety
    try:
        if operator == "==":
            if isinstance(user_val, str) and isinstance(expected_val, str):
                passed = (user_val.strip().lower() == expected_val.strip().lower())
            else:
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
            if isinstance(user_val, str) and isinstance(expected_val, str):
                passed = (user_val.strip().lower() != expected_val.strip().lower())
            else:
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
            u_num = _to_numeric(user_val)
            e_num = _to_numeric(expected_val)

            if u_num is not None and e_num is not None:
                if operator == ">":
                    passed = u_num > e_num
                elif operator == ">=":
                    passed = u_num >= e_num
                elif operator == "<":
                    passed = u_num < e_num
                elif operator == "<=":
                    passed = u_num <= e_num
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
            if isinstance(expected_val, (list, tuple, set)):
                passed = (user_val in expected_val) or (str(user_val).lower() in [str(x).lower() for x in expected_val])
            elif isinstance(user_val, (list, tuple, set)):
                passed = (expected_val in user_val) or (str(expected_val).lower() in [str(x).lower() for x in user_val])
            elif isinstance(expected_val, str) and isinstance(user_val, str):
                passed = user_val.lower() in expected_val.lower()
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
    scheme_or_criteria: Union[Dict[str, Any], Scheme, List[Any]],
) -> EvaluationResult:
    """
    Evaluates all criteria for a given scheme against the user profile.
    Deterministic Python evaluation — sole authority for eligibility.

    Supports both full Scheme models/dictionaries and legacy criteria lists.
    Returns EvaluationResult supporting both typed object attributes and dictionary access.
    """
    if isinstance(scheme_or_criteria, Scheme):
        scheme_id = scheme_or_criteria.id
        criteria_list = scheme_or_criteria.criteria
    elif isinstance(scheme_or_criteria, dict):
        scheme_id = str(scheme_or_criteria.get("id", scheme_or_criteria.get("scheme_id", "unknown_scheme")))
        criteria_list = scheme_or_criteria.get("criteria", [])
    elif isinstance(scheme_or_criteria, list):
        scheme_id = "custom_scheme"
        criteria_list = scheme_or_criteria
    else:
        validated = validate_scheme(scheme_or_criteria)
        scheme_id = validated.id
        criteria_list = validated.criteria

    criteria_results: List[CriterionResult] = []
    nodes: List[Dict[str, Any]] = []

    for crit in criteria_list:
        res = evaluate_criterion(profile, crit)
        criteria_results.append(res)

        # Build node structure for React Flow reasoning tree
        if isinstance(crit, dict):
            rule_label = crit.get("label") or f"{crit.get('field', '')} {crit.get('operator', '')} {crit.get('expected_value', '')}".strip()
        elif hasattr(crit, "label") and getattr(crit, "label"):
            rule_label = getattr(crit, "label")
        else:
            rule_label = f"{res.criterion_id} {res.operator} {res.expected_value}".strip()

        nodes.append({
            "id": res.criterion_id,
            "rule": rule_label,
            "user_val": res.user_value,
            "expected_val": res.expected_value,
            "status": "PASS" if res.status == CriterionStatus.PASS.value else ("MISSING" if res.status == CriterionStatus.MISSING_DATA.value else "FAIL"),
            "citation": res.citation,
            "reason": res.reason,
        })

    passed_count = sum(1 for r in criteria_results if r.status == CriterionStatus.PASS.value)
    failed_count = sum(1 for r in criteria_results if r.status == CriterionStatus.FAIL.value)
    missing_count = sum(1 for r in criteria_results if r.status == CriterionStatus.MISSING_DATA.value)
    total_count = len(criteria_list)

    # Derive overall status deterministically
    if failed_count > 0:
        overall_status = OverallStatus.NOT_ELIGIBLE.value
    elif missing_count > 0:
        overall_status = OverallStatus.INSUFFICIENT_DATA.value
    else:
        overall_status = OverallStatus.ELIGIBLE.value

    match_score = int((passed_count / total_count) * 100) if total_count > 0 else (100 if overall_status == OverallStatus.ELIGIBLE.value else 0)

    return EvaluationResult(
        scheme_id=scheme_id,
        overall_status=overall_status,
        criteria=criteria_results,
        nodes=nodes,
        passed_count=passed_count,
        failed_count=failed_count,
        missing_count=missing_count,
        total_count=total_count,
        match_score=match_score,
    )
