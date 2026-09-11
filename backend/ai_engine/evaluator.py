from typing import Any, Dict, List

def evaluate_criterion(profile: Dict[str, Any], criterion: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates a single criterion rule against a citizen's profile.
    Deterministic Python evaluation — zero LLM hallucination.
    """
    field = criterion.get("field")
    operator = criterion.get("operator", "==")
    expected_value = criterion.get("expected_value")
    citation = criterion.get("citation", {})
    label = criterion.get("label", field)

    user_val = profile.get(field)

    # Perform deterministic comparison
    passed = False
    if user_val is not None:
        try:
            if operator == "==":
                passed = (str(user_val).strip().lower() == str(expected_value).strip().lower()) if isinstance(expected_value, str) else (user_val == expected_value)
            elif operator == "!=":
                passed = user_val != expected_value
            elif operator == ">=":
                passed = float(user_val) >= float(expected_value)
            elif operator == "<=":
                passed = float(user_val) <= float(expected_value)
            elif operator == ">":
                passed = float(user_val) > float(expected_value)
            elif operator == "<":
                passed = float(user_val) < float(expected_value)
            elif operator == "in":
                if isinstance(expected_value, list):
                    passed = user_val in expected_value or str(user_val).lower() in [str(x).lower() for x in expected_value]
                else:
                    passed = str(user_val).lower() in str(expected_value).lower()
        except Exception as e:
            print(f"Error evaluating rule {field} {operator} {expected_value} for value {user_val}: {e}")
            passed = False

    return {
        "id": criterion.get("id", f"crit_{field}"),
        "rule": label or f"{field} {operator} {expected_value}",
        "user_val": user_val,
        "expected_val": expected_value,
        "status": "PASS" if passed else "FAIL",
        "citation": citation
    }

def evaluate_eligibility(profile: Dict[str, Any], scheme_criteria: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluates all criteria for a given scheme against the user profile.
    Returns structured node tree data ready for React Flow presentation.
    """
    if not scheme_criteria:
        return {
            "overall_status": "ELIGIBLE",
            "match_score": 100,
            "passed_count": 0,
            "total_count": 0,
            "nodes": []
        }

    nodes = []
    pass_count = 0

    for crit in scheme_criteria:
        result = evaluate_criterion(profile, crit)
        if result["status"] == "PASS":
            pass_count += 1
        nodes.append(result)

    total_count = len(scheme_criteria)
    overall_status = "ELIGIBLE" if pass_count == total_count else "INELIGIBLE"
    match_score = int((pass_count / total_count) * 100) if total_count > 0 else 0

    return {
        "overall_status": overall_status,
        "match_score": match_score,
        "passed_count": pass_count,
        "total_count": total_count,
        "nodes": nodes
    }
