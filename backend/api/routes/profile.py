"""
Profile route for CiviQ API.
Handles profile ingestion, validation, and real-time database persistence.
"""

import logging
import uuid
from typing import Any, Dict
from fastapi import APIRouter
from ..schemas import ProfileSchema

try:
    from ai_engine.db_client import get_client
except ImportError:
    from backend.ai_engine.db_client import get_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("")
async def save_profile_endpoint(profile: ProfileSchema) -> Dict[str, Any]:
    """
    Validates citizen profile and persists to Supabase in real-time.
    Gracefully falls back if database is temporarily offline.
    """
    profile_data = profile.model_dump()
    saved_to_db = False
    profile_id = str(uuid.uuid4())

    client = get_client()
    if client:
        try:
            # Map to Supabase table columns
            db_record = {
                "user_id": profile_data.get("user_id") or f"user_{profile_data.get('full_name', 'citizen').lower().replace(' ', '_')}_{str(uuid.uuid4())[:8]}",
                "full_name": profile_data.get("full_name", ""),
                "age": profile_data.get("age", 0),
                "gender": profile_data.get("gender", ""),
                "state": profile_data.get("state", ""),
                "district": profile_data.get("district", ""),
                "category": profile_data.get("category", ""),
                "annual_income": profile_data.get("annual_income", 0.0),
                "occupation": profile_data.get("occupation", ""),
                "is_bpl": profile_data.get("has_bpl_card", False),
                "is_disabled": profile_data.get("disability", False),
                "education_level": profile_data.get("education", ""),
                "marks_percentage": profile_data.get("marks_percentage"),
            }
            res = client.table("profiles").upsert(db_record).execute()
            if res.data:
                profile_id = res.data[0].get("id", profile_id)
                saved_to_db = True
                logger.info("Successfully persisted profile %s to Supabase", profile_id)
        except Exception as exc:
            logger.warning("Supabase profile persistence failed (operating locally): %s", exc)

    return {
        "status": "success",
        "profile_id": profile_id,
        "saved_to_database": saved_to_db,
        "profile": profile_data,
        **profile_data,
    }
