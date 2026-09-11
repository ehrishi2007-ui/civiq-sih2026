"""
CiviQ FastAPI Application Entrypoint.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .routes import api_v1_router
from .schemas import HealthResponse

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="CiviQ AI-Powered Government Scheme Navigator API",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 routes (/api/v1/profile, /api/v1/match)
app.include_router(api_v1_router)


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """System health check endpoint."""
    return HealthResponse(status="ok", version=settings.VERSION)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global fail-safe exception handler.
    Ensures internal stack traces are never leaked in API responses.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal server error occurred."},
    )
