"""
API Routes package.
"""

from fastapi import APIRouter
from .profile import router as profile_router
from .schemes import router as schemes_router
from .ask import router as ask_router
from .myths import router as myths_router
from .comparator import router as comparator_router
from .translate import router as translate_router
from .policy import router as policy_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(profile_router)
api_v1_router.include_router(schemes_router)
api_v1_router.include_router(ask_router)
api_v1_router.include_router(myths_router)
api_v1_router.include_router(comparator_router)
api_v1_router.include_router(translate_router)
api_v1_router.include_router(policy_router)

__all__ = [
    "api_v1_router",
    "profile_router",
    "schemes_router",
    "ask_router",
    "myths_router",
    "comparator_router",
    "translate_router",
    "policy_router",
]
