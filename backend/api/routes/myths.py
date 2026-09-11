"""
Myth Buster / Misinformation Check Route for CiviQ.
"""

from fastapi import APIRouter, status

from ..schemas import MythCheckRequest, MythCheckResponse

try:
    from ai_engine.myth_checker import check_myth
except ImportError:
    from backend.ai_engine.myth_checker import check_myth

router = APIRouter(prefix="/myths", tags=["myths"])


@router.post("/check", response_model=MythCheckResponse, status_code=status.HTTP_200_OK)
async def check_claim(payload: MythCheckRequest) -> MythCheckResponse:
    """
    Checks citizen inquiry or rumor against curated scheme registry.
    Returns verified facts, canonical verdict, and official citations.
    """
    result = check_myth(query=payload.claim)
    return MythCheckResponse(
        verdict=result.get("verdict", "UNVERIFIED"),
        explanation=result.get("explanation", ""),
        sources=result.get("sources", []),
        warning=result.get("warning"),
        real_scheme=result.get("real_scheme"),
        real_facts=result.get("real_facts"),
        citation=result.get("citation"),
    )
