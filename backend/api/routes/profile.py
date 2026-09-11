"""
Profile route for CiviQ API.
Handles profile ingestion and validation.
"""

from typing import Any, Dict
from fastapi import APIRouter
from ..schemas import ProfileSchema

router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("")
async def validate_profile(profile: ProfileSchema) -> Dict[str, Any]:
    """
    Validates an arbitrary citizen profile against the canonical profile schema.
    Returns the validated profile without database persistence.
    """
    profile_data = profile.model_dump()
    return {
        "status": "success",
        "profile": profile_data,
        **profile_data,
    }
