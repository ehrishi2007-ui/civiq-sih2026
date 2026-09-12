"""
Unit and Integration Tests for Tavily Autonomous Policy Ingestion Pipeline.
Validates:
1. Strict domain whitelist (*.gov.in and *.nic.in).
2. Non-government domains are strictly rejected.
3. Tavily tracker extracts structured diff adhering to schema.
4. Deterministic evaluator recalculates citizen eligibility without hallucination.
5. POST /api/v1/policy/auto-update returns HTTP 200 with valid schema.
6. GET /api/v1/policy/freshness-feed returns valid circulars.
"""

import pytest
from fastapi.testclient import TestClient

from api.main import app
from ai_engine.tavily_tracker import TavilyPolicyTracker, is_allowed_gov_domain
from ai_engine.auto_updater import PolicyAutoUpdater, DEMO_STUDENT_PROFILE

client = TestClient(app)


def test_zero_trust_domain_whitelisting():
    assert is_allowed_gov_domain("https://pib.gov.in/PressReleasePage.aspx?PRID=123") is True
    assert is_allowed_gov_domain("https://mha.gov.in/circulars/pmss.pdf") is True
    assert is_allowed_gov_domain("https://scholarships.gov.in/home") is True
    assert is_allowed_gov_domain("https://nic.in/announcements") is True
    
    # Non-government and commercial sites must be rejected
    assert is_allowed_gov_domain("https://google.com/search") is False
    assert is_allowed_gov_domain("https://fake-scheme-apply.com") is False
    assert is_allowed_gov_domain("https://gov.in.scamdomain.com") is False
    assert is_allowed_gov_domain("") is False


def test_tavily_tracker_discovery_and_diff():
    tracker = TavilyPolicyTracker()
    results = tracker.search_policy_updates(scheme_name="PM Scholarship", year=2026)
    assert len(results) >= 1
    assert "pib.gov.in" in results[0]["url"] or is_allowed_gov_domain(results[0]["url"])

    diff = tracker.extract_policy_diff(results[0]["content"])
    assert diff["has_changes"] is True
    assert diff["version_year"] == "2026-27"
    assert len(diff["changes"]) >= 2
    parameters = [c["parameter"] for c in diff["changes"]]
    assert any("Girls" in p for p in parameters)
    assert any("Income" in p for p in parameters)


def test_auto_updater_eligibility_flip():
    updater = PolicyAutoUpdater()
    res = updater.run_auto_update(citizen_profile=DEMO_STUDENT_PROFILE)
    
    assert res["success"] is True
    impact = res["citizen_impact"]
    assert impact["status_before"] == "NOT_ELIGIBLE"
    assert impact["status_after"] == "ELIGIBLE"
    assert impact["eligibility_flipped"] is True
    assert impact["annual_financial_gain"] == 7200
    assert impact["total_new_annual_benefit"] == 43200
    assert "BREAKING UPDATE" in impact["citizen_alert"]


def test_api_policy_auto_update_endpoint():
    payload = {
        "scheme_id": "pm_scholarship_warb",
        "citizen_profile": DEMO_STUDENT_PROFILE,
    }
    response = client.post("/api/v1/policy/auto-update", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["citizen_impact"]["eligibility_flipped"] is True
    assert data["evaluator_authority"] == "Pure Python evaluator.py (Zero LLM Hallucination)"


def test_api_policy_freshness_feed_endpoint():
    response = client.get("/api/v1/policy/freshness-feed")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 1
    assert "Autonomous Tavily" in data["source"]
