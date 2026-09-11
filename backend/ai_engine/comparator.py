from typing import Any, Dict, List, Optional

def compare_policy_versions(scheme_data: Dict[str, Any], user_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Compares 2022 vs 2024 scheme policy changes and generates personalized impact summaries.
    """
    policy_diff = scheme_data.get("policy_diff", {})
    changes = policy_diff.get("changes", [])

    diff_matrix = []
    personalized_impact = "Review the latest policy revisions below to see updated benefits."

    for change in changes:
        param = change.get("parameter", "")
        old_val = change.get("old_value", "")
        new_val = change.get("new_value", "")
        impact_tag = change.get("impact_tag", "Policy Revision")

        diff_matrix.append({
            "param": param,
            "old_val": old_val,
            "new_val": new_val,
            "change": impact_tag
        })

    # If user profile is provided, personalize the impact statement
    if user_profile:
        gender = str(user_profile.get("gender", "")).lower()
        income = user_profile.get("annual_income", 0)
        
        # Example personalized heuristics for PMSS demo
        if gender == "female" or gender == "girl":
            personalized_impact = "Because of the 2024 revision, your monthly stipend increased from ₹3,000 to ₹3,600 (an extra ₹7,200 annually)."
        elif income and income > 600000 and income <= 800000:
            personalized_impact = "The income cap was relaxed to ₹8,00,000 per annum, making you newly eligible for this assistance!"

    return {
        "scheme_id": scheme_data.get("id", ""),
        "version_old": policy_diff.get("previous_version", "2022-23"),
        "version_new": policy_diff.get("current_version", "2024-25"),
        "diff_matrix": diff_matrix,
        "personalized_impact": personalized_impact
    }
