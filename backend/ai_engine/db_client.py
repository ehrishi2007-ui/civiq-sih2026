"""
Optional Supabase Database Client Adapter for CiviQ.
Provides safe, lazy initialization and helper methods without coupling
core evaluation, RAG, myth-busting, or scheme data to an external database.
"""

import logging
from typing import Any, Optional

try:
    from api.config import settings
except ImportError:
    from backend.api.config import settings

logger = logging.getLogger(__name__)

# Safe optional import of supabase-py
try:
    from supabase import Client, create_client
    _SUPABASE_AVAILABLE = True
except ImportError:
    create_client = None
    Client = Any
    _SUPABASE_AVAILABLE = False

_client_instance: Optional[Any] = None
_initialized: bool = False


def get_client() -> Optional[Any]:
    """
    Lazily initialize and return the Supabase client if credentials and
    the supabase package are available.
    Returns None safely if credentials are not configured or package is absent.
    """
    global _client_instance, _initialized
    if _initialized:
        return _client_instance

    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY

    if not url or not key:
        logger.info("Supabase credentials not configured; operating in local/offline mode.")
        _client_instance = None
        _initialized = True
        return None

    if not _SUPABASE_AVAILABLE or create_client is None:
        logger.warning("supabase package is not installed; Supabase client unavailable.")
        _client_instance = None
        _initialized = True
        return None

    try:
        _client_instance = create_client(url, key)
        logger.info("Supabase client successfully initialized.")
    except Exception as exc:
        logger.warning("Failed to initialize Supabase client: %s", exc)
        _client_instance = None

    _initialized = True
    return _client_instance


def is_connected() -> bool:
    """
    Returns True if a Supabase client has been successfully initialized.
    """
    return get_client() is not None


def reset_client() -> None:
    """
    Reset client state (primarily for tests and dynamic configuration).
    """
    global _client_instance, _initialized
    _client_instance = None
    _initialized = False
