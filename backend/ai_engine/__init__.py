"""
CiviQ AI Engine Package.
Unified interface for data models, deterministic eligibility evaluator, RAG policy intelligence,
comparator, myth checker, and translation services.
"""

from .schemas import (
    Citation,
    Criterion,
    Scheme,
    CriterionStatus,
    OverallStatus,
    CriterionResult,
    EvaluationResult,
    validate_scheme,
    validate_schemes_list,
)
from .evaluator import (
    evaluate_eligibility,
    evaluate_criterion,
    SUPPORTED_OPERATORS,
)
from .comparator import compare_policy_versions
from .myth_checker import check_myth
from .rag import ask_policy
from .translator import translate_texts
from .db_client import supabase
from .vector_store import upload_all_pdfs, get_uploaded_files

__all__ = [
    # Schemas & Contracts
    "Citation",
    "Criterion",
    "Scheme",
    "CriterionStatus",
    "OverallStatus",
    "CriterionResult",
    "EvaluationResult",
    "validate_scheme",
    "validate_schemes_list",
    # Evaluator
    "evaluate_eligibility",
    "evaluate_criterion",
    "SUPPORTED_OPERATORS",
    # Feature Engines
    "compare_policy_versions",
    "check_myth",
    "ask_policy",
    "translate_texts",
    # Storage & DB
    "supabase",
    "upload_all_pdfs",
    "get_uploaded_files",
]
