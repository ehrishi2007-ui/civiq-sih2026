"""
CiviQ Backend Configuration.
"""

import os
from pathlib import Path
from typing import List


class Settings:
    PROJECT_NAME: str = "CiviQ API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",
    ]
    DATA_DIR: Path = Path(__file__).resolve().parent.parent.parent / "data"
    SCHEMES_FILE: Path = DATA_DIR / "schemes_extracted.json"
    MYTHS_FILE: Path = DATA_DIR / "myths.json"
    RAW_PDFS_DIR: Path = DATA_DIR / "raw_pdfs"
    UPLOADED_FILES_REGISTRY: Path = Path(__file__).resolve().parent.parent / "ai_engine" / "uploaded_files.json"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    GOOGLE_TRANSLATE_API_KEY: str = os.getenv("GOOGLE_TRANSLATE_API_KEY", "")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")


settings = Settings()

