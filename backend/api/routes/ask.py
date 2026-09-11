"""
Policy Intelligence Ask Route for CiviQ.
"""

from fastapi import APIRouter, status

from ..schemas import AskRequest, AskResponse

try:
    from ai_engine.rag import ask_policy
except ImportError:
    from backend.ai_engine.rag import ask_policy

router = APIRouter(tags=["ask"])


@router.post("/ask", response_model=AskResponse, status_code=status.HTTP_200_OK)
async def ask_civiq(payload: AskRequest) -> AskResponse:
    """
    Grounded policy question answering endpoint.
    Answers citizen questions strictly grounded in official scheme documents.
    """
    result = ask_policy(question=payload.question, context=payload.context)
    return AskResponse(
        answer=result.get("answer", ""),
        sources=result.get("sources", []),
    )
