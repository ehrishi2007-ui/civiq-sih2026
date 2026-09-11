"""
CiviQ Backend - Scheme and Evaluator Data Contracts.
Defines schemas for schemes, criteria, citations, and evaluation results.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict, Field


class Citation(BaseModel):
    """Citation linking a criterion directly to its official source document."""
    model_config = ConfigDict(extra="ignore")

    doc_name: str
    page: Union[int, str]
    section: str
    quote: str

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


class Criterion(BaseModel):
    """Single eligibility rule defined for a scheme."""
    model_config = ConfigDict(extra="ignore")

    id: str
    field: str
    operator: str
    expected_value: Any
    citation: Optional[Citation] = None
    label: Optional[str] = None

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


class Scheme(BaseModel):
    """Canonical data model for a government scheme."""
    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    ministry: str
    short_desc: str
    benefit_summary: str
    application_url: str
    closing_date: Optional[str] = None
    version_year: int = 2024
    criteria: List[Criterion] = Field(default_factory=list)
    policy_diff: Optional[Dict[str, Any]] = None

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


class CriterionStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    MISSING_DATA = "MISSING_DATA"


class OverallStatus(str, Enum):
    ELIGIBLE = "ELIGIBLE"
    NOT_ELIGIBLE = "NOT_ELIGIBLE"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class CriterionResult(BaseModel):
    """Evaluation outcome for an individual criterion."""
    model_config = ConfigDict(extra="ignore")

    criterion_id: str
    status: str  # "PASS", "FAIL", "MISSING_DATA"
    user_value: Any = None
    expected_value: Any = None
    operator: str
    citation: Dict[str, Any] = Field(default_factory=dict)
    reason: Optional[str] = None

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def get(self, item: str, default: Any = None) -> Any:
        return getattr(self, item, default)


class EvaluationResult(BaseModel):
    """
    Comprehensive, deterministic evaluation outcome for a scheme against a profile.
    Supports both object attribute access and dictionary access for full caller compatibility.
    """
    model_config = ConfigDict(extra="ignore")

    scheme_id: str
    overall_status: str  # "ELIGIBLE", "NOT_ELIGIBLE", "INSUFFICIENT_DATA"
    criteria: List[CriterionResult] = Field(default_factory=list)
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    passed_count: int = 0
    failed_count: int = 0
    missing_count: int = 0
    total_count: int = 0
    match_score: int = 0

    @property
    def results(self) -> List[CriterionResult]:
        return self.criteria

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def get(self, item: str, default: Any = None) -> Any:
        return getattr(self, item, default)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()


def validate_scheme(data: Union[Dict[str, Any], Scheme]) -> Scheme:
    """Validates and returns a typed Scheme object from a dictionary or instance."""
    if isinstance(data, Scheme):
        return data
    return Scheme.model_validate(data)


def validate_schemes_list(data: List[Any]) -> List[Scheme]:
    """Validates a list of scheme dictionaries against the canonical scheme contract."""
    return [validate_scheme(item) for item in data]
