"""
Policy Version Comparator Route for CiviQ.
"""

from fastapi import APIRouter, status

from ..schemas import ComparatorRequest, ComparatorResponse

try:
    from ai_engine.comparator import compare_policy_versions
except ImportError:
    from backend.ai_engine.comparator import compare_policy_versions

router = APIRouter(tags=["comparator"])


@router.post("/comparator", response_model=ComparatorResponse, status_code=status.HTTP_200_OK)
async def compare_policy(payload: ComparatorRequest) -> ComparatorResponse:
    """
    Compares scheme policy guidelines between verified historical and updated versions.
    Explains verified changes and evaluates profile-specific eligibility impacts.
    """
    result = compare_policy_versions(
        user_profile=payload.user_profile,
        scheme_id=payload.scheme_id,
    )
    return ComparatorResponse(**result)
