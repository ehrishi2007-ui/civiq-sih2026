"""
API Routes package.
"""

from fastapi import APIRouter
from .profile import router as profile_router
from .schemes import router as schemes_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(profile_router)
api_v1_router.include_router(schemes_router)

__all__ = ["api_v1_router", "profile_router", "schemes_router"]
