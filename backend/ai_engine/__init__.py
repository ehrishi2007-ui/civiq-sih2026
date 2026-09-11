"""
CiviQ AI Engine Package.
Unified interface for data models, deterministic eligibility evaluator, RAG policy intelligence,
comparator, myth checker, and translation services.
"""

from .schemas import (
    Citation,
    Criterion,
    Scheme,
    CriterionResult,
    EvaluationResult,
    CriterionStatus,
    OverallStatus,
    validate_scheme,
    validate_schemes_list,
)
from .evaluator import (
    evaluate_eligibility,
    evaluate_criterion,
    SUPPORTED_OPERATORS,
)
from .pdf_service import (
    APPROVED_MVP_PDFS,
    EXCLUDED_PDFS,
    PDFServiceError,
    MissingPDFError,
    GeminiAuthError,
    GeminiUploadError,
    discover_approved_pdfs,
    load_registry,
    save_registry,
    ingest_official_pdfs,
    get_official_pdf_handles,
)
from .rag import ask_policy, extract_citations, SYSTEM_INSTRUCTION
from .vector_store import get_uploaded_files, upload_all_pdfs
from .myth_checker import check_myth, load_myths, map_verdict
from .comparator import compare_policy_versions
from .translator import (
    SUPPORTED_LANGUAGES,
    VALID_TARGET_LANGUAGES,
    translate_text,
    translate_texts,
    translate_text_with_meta,
    clear_cache,
)
from .db_client import get_client, is_connected, reset_client

__all__ = [
    # Schemas & Contracts
    "Citation",
    "Criterion",
    "Scheme",
    "CriterionResult",
    "EvaluationResult",
    "CriterionStatus",
    "OverallStatus",
    "validate_scheme",
    "validate_schemes_list",
    # Evaluator
    "evaluate_eligibility",
    "evaluate_criterion",
    "SUPPORTED_OPERATORS",
    # PDF Ingestion & Discovery
    "APPROVED_MVP_PDFS",
    "EXCLUDED_PDFS",
    "PDFServiceError",
    "MissingPDFError",
    "GeminiAuthError",
    "GeminiUploadError",
    "discover_approved_pdfs",
    "load_registry",
    "save_registry",
    "ingest_official_pdfs",
    "get_official_pdf_handles",
    # RAG & Evidence
    "ask_policy",
    "extract_citations",
    "SYSTEM_INSTRUCTION",
    "get_uploaded_files",
    "upload_all_pdfs",
    # Myth Buster
    "check_myth",
    "load_myths",
    "map_verdict",
    # Comparator
    "compare_policy_versions",
    # Translation
    "SUPPORTED_LANGUAGES",
    "VALID_TARGET_LANGUAGES",
    "translate_text",
    "translate_texts",
    "translate_text_with_meta",
    "clear_cache",
    # Database
    "get_client",
    "is_connected",
    "reset_client",
]
