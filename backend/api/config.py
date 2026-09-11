"""
CiviQ Backend Configuration.
"""

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


settings = Settings()
