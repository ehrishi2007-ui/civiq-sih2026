"""
CiviQ FastAPI Application Entrypoint.
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

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


@app.get("/api/v1/documents/{filename}", tags=["documents"])
async def get_document(filename: str):
    """
    Serves official policy PDF documents for citation verification.
    Streams raw PDF files inline with proper content-type.
    """
    safe_name = filename.strip().replace("..", "").replace("/", "").replace("\\", "")
    pdf_path = settings.RAW_PDFS_DIR / safe_name
    if not pdf_path.exists():
        for p in settings.RAW_PDFS_DIR.glob("*.pdf"):
            if p.name.lower() == safe_name.lower():
                pdf_path = p
                break
    if not pdf_path.exists() or not pdf_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Official document '{filename}' not found on server.",
        )
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=\"{pdf_path.name}\""},
    )


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
