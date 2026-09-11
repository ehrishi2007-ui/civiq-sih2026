"""
CiviQ M7 - Policy Comparator Engine.

Responsible for:
1. Comparing scheme policy versions between verified historical guidelines and updated guidelines.
2. For MVP: Primary focus is PMSS (2023-24 vs 2026-27).
3. Grounding rule: PMSS 2026-27.pdf is a scanned image PDF with zero extractable digital text.
   Comparison evidence is handled conservatively (no fabricated differences or citations).
4. Evaluator integration: Uses the deterministic evaluator to report verified eligibility impact.
   Never replaces or overrides deterministic evaluator decisions.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from api.config import settings
except ImportError:
    from backend.api.config import settings

try:
    from .evaluator import evaluate_eligibility
except ImportError:
    from ai_engine.evaluator import evaluate_eligibility


def _load_scheme_by_id(scheme_id: str) -> Optional[Dict[str, Any]]:
    """Loads scheme definition from canonical data/schemes_extracted.json."""
    schemes_file = getattr(settings, "SCHEMES_FILE", None)
    if not schemes_file or not schemes_file.exists():
        schemes_file = Path(__file__).resolve().parent.parent.parent / "data" / "schemes_extracted.json"

    if not schemes_file.exists():
        return None

    try:
        with open(schemes_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                for s in data:
                    if s.get("id") == scheme_id:
                        return s
    except Exception:
        pass
    return None


def compare_policy_versions(
    scheme_data: Optional[Dict[str, Any]] = None,
    user_profile: Optional[Dict[str, Any]] = None,
    scheme_id: str = "pm_scholarship_warb",
) -> Dict[str, Any]:
    """
    Compares scheme policy versions.
    For PMSS, compares 2023-24 vs 2026-27.
    Returns structured comparison response conforming to CiviQ contract.
    """
    # Resolve scheme data
    target_data = scheme_data
    if target_data is None:
        target_data = _load_scheme_by_id(scheme_id)

    # Defaults for PMSS
    sid = target_data.get("id", scheme_id) if target_data else scheme_id
    sname = target_data.get("name", "Prime Minister's Scholarship Scheme (WARB)") if target_data else "Prime Minister's Scholarship Scheme (WARB)"

    old_version = "2023-24"
    new_version = "2026-27"

    # Check if target_data has policy_diff
    policy_diff = (target_data or {}).get("policy_diff")

    # If policy_diff is present and has verified changes
    if policy_diff and isinstance(policy_diff, dict) and policy_diff.get("changes"):
        raw_changes = policy_diff.get("changes", [])
        changes = []
        diff_matrix = []
        for c in raw_changes:
            param = c.get("field") or c.get("parameter") or c.get("param", "")
            old_val = str(c.get("old_value", c.get("old_val", "")))
            new_val = str(c.get("new_value", c.get("new_val", "")))
            change_lbl = c.get("change_label", c.get("impact_tag", c.get("change", "Policy Revision")))
            direction = c.get("direction", "neutral")
            impact = c.get("impact", "")
            sources = c.get("sources", [])

            item = {
                "field": param,
                "param": param,
                "old_value": old_val,
                "old_val": old_val,
                "new_value": new_val,
                "new_val": new_val,
                "change_label": change_lbl,
                "change": change_lbl,
                "direction": direction,
                "impact": impact,
                "sources": sources,
            }
            changes.append(item)
            diff_matrix.append(item)

        verified = True
        status_code = "VERIFIED"
        message = "Verified policy differences between guidelines."
        sources = policy_diff.get("sources", [])
    else:
        # Conservative handling for PMSS 2026-27 (scanned PDF without digital text)
        changes = []
        diff_matrix = []
        verified = False
        status_code = "UNVERIFIED_NEW_VERSION"
        message = (
            "Comparison between PMSS 2023-24 and 2026-27 is pending OCR/multimodal verification. "
            "PMSS 2026-27.pdf is a scanned image document with zero extractable digital text; "
            "no policy differences are asserted to prevent fabricating ungrounded comparisons."
        )
        sources = [
            {
                "document": "PMSS 2023-24.pdf",
                "doc_name": "PMSS 2023-24.pdf",
                "page": 4,
                "section": "Clause 6: Amount of Scholarship",
                "quote": "Rs. 3000/- per month for girls. Rs. 2500/- per month for boys.",
            }
        ]

    # Evaluator Integration: evaluate user profile against verified 2023-24 rules
    personalized_impact = (
        f"Policy comparison between {old_version} and {new_version} requires document-level multimodal verification."
    )
    if user_profile and target_data:
        try:
            eval_result = evaluate_eligibility(user_profile, target_data)
            status_text = eval_result.overall_status
            personalized_impact = (
                f"Under verified {old_version} policy guidelines, your evaluated status is {status_text}. "
                f"Impact of {new_version} cannot be asserted until the scanned document is verified via OCR/multimodal ingestion."
            )
        except Exception:
            personalized_impact = (
                f"Under verified {old_version} policy, profile eligibility evaluation is available. "
                f"Changes for {new_version} remain unverified."
            )

    return {
        "scheme_id": sid,
        "scheme_name": sname,
        "old_version": old_version,
        "new_version": new_version,
        "version_old": old_version,
        "version_new": new_version,
        "verified": verified,
        "status": status_code,
        "message": message,
        "changes": changes,
        "diff_matrix": diff_matrix,
        "personalized_impact": personalized_impact,
        "sources": sources,
    }


if __name__ == "__main__":
    res = compare_policy_versions()
    print("--- PMSS COMPARISON ---")
    print(f"Scheme: {res['scheme_name']}")
    print(f"Versions: {res['old_version']} vs {res['new_version']}")
    print(f"Status: {res['status']}")
    print(f"Message: {res['message']}")
    print(f"Sources: {res['sources']}")
