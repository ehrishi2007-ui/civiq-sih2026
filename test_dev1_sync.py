"""
Test script to verify Dev 1 sync: Evaluator, Schemas, Schemes, and Myths.
"""
import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

print("=" * 60)
print("RUNNING DEV 1 SYNC & COMPLIANCE VERIFICATION")
print("=" * 60)

# 1. Test schemas and data validation
print("\n[1] Validating data/schemes_extracted.json...")
from backend.ai_engine.schemas import validate_schemes_list, Scheme, CriterionStatus, OverallStatus

with open("data/schemes_extracted.json", "r", encoding="utf-8") as f:
    schemes_data = json.load(f)

schemes = validate_schemes_list(schemes_data)
print(f"    ✓ Loaded and validated {len(schemes)} schemes.")
for s in schemes:
    print(f"      • {s.id}: {s.name} ({len(s.criteria)} criteria)")

# 2. Test Priya Ramesh Canonical Persona against PMSS
print("\n[2] Testing Evaluator with Priya Ramesh Canonical Persona...")
from backend.ai_engine.evaluator import evaluate_eligibility, evaluate_criterion

pmss = next(s for s in schemes_data if s["id"] == "pm_scholarship_warb")

priya = {
    "full_name": "Priya Ramesh",
    "occupation": "Student",
    "annual_income": 300000,
    "marks_percentage": 85,
    "gender": "Female"
}

# Test with criteria list
res_list = evaluate_eligibility(priya, pmss["criteria"])
print(f"    ✓ Evaluation with criteria list:")
print(f"      - Overall Status: {res_list.overall_status} (Dict access: {res_list['overall_status']})")
print(f"      - Match Score   : {res_list.match_score}% (Dict access: {res_list['match_score']}%)")
print(f"      - Nodes count   : {len(res_list.nodes)} (Dict access: {len(res_list['nodes'])})")
print(f"      - Passed/Total  : {res_list.passed_count}/{res_list.total_count}")
assert res_list.overall_status == OverallStatus.ELIGIBLE.value
assert res_list.match_score == 100
assert len(res_list.nodes) == 3
for n in res_list.nodes:
    assert n["status"] == "PASS"
    assert "citation" in n and n["citation"]["quote"]

# Test with full scheme object
res_scheme = evaluate_eligibility(priya, pmss)
print(f"    ✓ Evaluation with full scheme dict:")
print(f"      - Scheme ID     : {res_scheme.scheme_id}")
print(f"      - Overall Status: {res_scheme.overall_status}")
assert res_scheme.overall_status == OverallStatus.ELIGIBLE.value

# 3. Test Failure Condition (Income too high)
print("\n[3] Testing Failure Condition (High Income)...")
rich_profile = {
    "full_name": "Test User",
    "occupation": "Student",
    "annual_income": 1200000,  # exceeds 8L limit
    "marks_percentage": 85,
}
res_fail = evaluate_eligibility(rich_profile, pmss)
print(f"    ✓ Status for Income ₹12L: {res_fail.overall_status}")
assert res_fail.overall_status == OverallStatus.NOT_ELIGIBLE.value
assert res_fail.failed_count == 1
assert res_fail.passed_count == 2

# 4. Test Missing Data Condition (Field missing or None)
print("\n[4] Testing Missing Data Condition (Missing Marks)...")
incomplete_profile = {
    "full_name": "Test User",
    "occupation": "Student",
    "annual_income": 300000,
    # "marks_percentage" is missing
}
res_missing = evaluate_eligibility(incomplete_profile, pmss)
print(f"    ✓ Status for Missing Marks: {res_missing.overall_status}")
assert res_missing.overall_status == OverallStatus.INSUFFICIENT_DATA.value
assert res_missing.missing_count == 1
assert res_missing.failed_count == 0

# 5. Test Comparator
print("\n[5] Testing Comparator Personalization...")
from backend.ai_engine.comparator import compare_policy_versions
comp_res = compare_policy_versions(pmss, priya)
print(f"    ✓ Personalized Impact: {comp_res['personalized_impact']}")
print(f"    ✓ Diff changes: {len(comp_res['diff_matrix'])}")
assert len(comp_res["diff_matrix"]) == 2

# 6. Test Myth Checker
print("\n[6] Testing Myth Checker...")
from backend.ai_engine.myth_checker import check_myth
m_res = check_myth("modi 50000 farmers")
print(f"    ✓ Verdict: {m_res['verdict']} for scheme {m_res['real_scheme']}")
assert m_res["verdict"] == "FAKE"

print("\n" + "=" * 60)
print("✅ ALL DEV 1 SYNC TESTS PASSED PERFECTLY!")
print("=" * 60)
