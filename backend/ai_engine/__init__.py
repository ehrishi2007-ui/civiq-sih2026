"""
CiviQ AI Engine Package.
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
from .evaluator import evaluate_eligibility, SUPPORTED_OPERATORS

__all__ = [
    "Citation",
    "Criterion",
    "Scheme",
    "CriterionResult",
    "EvaluationResult",
    "CriterionStatus",
    "OverallStatus",
    "validate_scheme",
    "validate_schemes_list",
    "evaluate_eligibility",
    "SUPPORTED_OPERATORS",
]
