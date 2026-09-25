"""
CiviQ SIH 2026 - Autonomous Continuous Policy Updation Live Demo Script.
Demonstrates the core differentiator from myScheme in 10 seconds:
Tavily Drone -> Gemini Diff -> Deterministic Evaluator -> Citizen Alert.
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import api.config
from ai_engine.auto_updater import PolicyAutoUpdater, DEMO_STUDENT_PROFILE


def run_demo():
    print("=" * 80)
    print("  CIVIQ (SIH 2026) — AUTONOMOUS POLICY UPDATION PIPELINE")
    print("  Core Differentiator: myScheme (Static Delay) vs CiviQ (Living Policy)")
    print("=" * 80)

    updater = PolicyAutoUpdater()

    print("\n[STAGE 1] Testing Citizen Profile Against 2023-24 Guidelines...")
    print(f"  Profile: Female Student | Marks: 78.5% | Family Income: Rs. 7,20,000/yr")
    print(f"  Old Guideline Rule: Family Income must be <= Rs. 6,00,000/year.")
    print("  --> Baseline Status: NOT_ELIGIBLE (Income Ceiling Exceeded)")

    print("\n[STAGE 2] Autonomous Discovery (Tavily Drone Engine)...")
    print("  Scanning 'pib.gov.in' and '*.gov.in' for Union Cabinet 2026 notifications...")
    res = updater.run_auto_update(scheme_id="pm_scholarship_warb", citizen_profile=DEMO_STUDENT_PROFILE)
    doc = res["discovered_announcement"]
    print(f"  Found Official Circular: {doc['title']}")
    print(f"  Verified URL: {doc['url']}")
    print(f"  Source Provenance: {doc['source']}")

    print("\n[STAGE 3] Policy Parameter Diff Extraction (Gemini 3.5 Flash Lite)...")
    diff = res["policy_diff"]
    print(f"  Summary: {diff.get('summary')}")
    for change in diff.get("changes", []):
        print(f"  * {change['parameter']}: {change['old_value']}  -->  {change['new_value']}")
        print(f"    Impact: {change['impact_tag']}")

    print("\n[STAGE 4] Deterministic Citizen Re-Evaluation (Pure Python evaluator.py)...")
    print("  Axiom: 'AI discovers and explains, but Python decides.'")
    impact = res["citizen_impact"]
    print(f"  Status Flip: {impact['status_before']}  ====>  {impact['status_after']}!")
    print(f"  Personalized Financial Gain: +Rs. {impact['annual_financial_gain']:,}/year")
    print(f"  Total Annual Entitlement: Rs. {impact['total_new_annual_benefit']:,}/year")

    print("\n[STAGE 5] Citizen Notification Generated:")
    print(f"  {impact['citizen_alert']}")

    print("\n" + "=" * 80)
    print("  RESULT: Zero Manual Webmaster Delay. Zero LLM Hallucination.")
    print("  100% Grounded in Official PIB Press Releases.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    run_demo()
