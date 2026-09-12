"""
CiviQ API - Autonomous Policy Ingestion & Feed Router.
Exposes endpoints to trigger Tavily continuous policy ingestion
and inspect live government freshness feeds.
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from ai_engine.auto_updater import PolicyAutoUpdater
from ai_engine.tavily_tracker import TavilyPolicyTracker

router = APIRouter(prefix="/policy", tags=["policy"])


class AutoUpdateRequest(BaseModel):
    scheme_id: str = Field(default="pm_scholarship_warb", description="Scheme identifier to check and update")
    citizen_profile: Optional[Dict[str, Any]] = Field(default=None, description="Optional citizen profile to test impact")


class AutoUpdateResponse(BaseModel):
    success: bool
    scheme_id: str
    scheme_name: Optional[str] = None
    discovered_announcement: Dict[str, Any]
    policy_diff: Dict[str, Any]
    citizen_impact: Dict[str, Any]
    evaluator_authority: str


@router.post(
    "/auto-update",
    response_model=AutoUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Autonomous Policy Updation & Citizen Re-evaluation",
)
def trigger_policy_auto_update(req: AutoUpdateRequest):
    """
    Executes the autonomous policy ingestion pipeline:
    1. Scans PIB / .gov.in via Tavily Drone Engine
    2. Extracts structured parameter diffs via Gemini 3.5
    3. Re-evaluates citizen eligibility via deterministic evaluator
    4. Calculates personalized Rs delta gain and generates instant citizen alert
    """
    updater = PolicyAutoUpdater()
    result = updater.run_auto_update(scheme_id=req.scheme_id, citizen_profile=req.citizen_profile)
    return AutoUpdateResponse(**result)


@router.get(
    "/freshness-feed",
    status_code=status.HTTP_200_OK,
    summary="Live Government Notification Feed",
)
def get_freshness_feed():
    """
    Returns real-time policy alerts and PIB notifications discovered across official .gov.in domains.
    """
    tracker = TavilyPolicyTracker()
    circulars = tracker.search_policy_updates("PM Scholarship 2026")
    return {
        "count": len(circulars),
        "source": "Autonomous Tavily Gov.in Discovery Engine",
        "feed": circulars,
    }
