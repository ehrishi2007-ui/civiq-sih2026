"""
API Request and Response Pydantic Schemas for CiviQ.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ProfileSchema(BaseModel):
    """Citizen profile schema for scheme matching."""
    model_config = ConfigDict(extra="allow")

    full_name: str = Field(..., min_length=1, description="Full name of applicant")
    age: int = Field(..., ge=0, le=130, description="Age in completed years")
    gender: str = Field(..., min_length=1, description="Gender (male, female, other)")
    category: str = Field(..., min_length=1, description="Social category (General, OBC, SC, ST)")
    annual_income: float = Field(..., ge=0, description="Total annual family income in INR")
    state: str = Field(..., min_length=1, description="State of residence")
    district: str = Field(..., min_length=1, description="District of residence")
    is_rural: bool = Field(..., description="Whether residing in rural area")
    occupation: str = Field(..., min_length=1, description="Primary occupation")
    education: str = Field(..., min_length=1, description="Highest educational attainment")
    has_land: bool = Field(..., description="Whether family owns cultivable land")
    land_acres: Optional[float] = Field(default=0.0, ge=0, description="Land area in acres")
    has_bpl_card: bool = Field(..., description="Whether family holds Below Poverty Line card")
    disability: Optional[bool] = Field(default=False, description="Person with disability status")
    minority: Optional[bool] = Field(default=False, description="Minority community status")
    ration_card_type: Optional[str] = Field(default="None", description="Ration card type (e.g. None, PHH, AAY)")
    documents: Optional[List[str]] = Field(default_factory=list, description="List of verified documents available")


class HealthResponse(BaseModel):
    """System health check response."""
    status: str = "ok"
    version: str = "1.0.0"


class CriterionMatchResult(BaseModel):
    """Evaluated criterion result for API response."""
    model_config = ConfigDict(extra="ignore")

    criterion_id: str
    field: str
    status: str  # PASS | FAIL | MISSING_DATA
    pass_status: bool  # True if PASS
    user_value: Any = None
    expected_value: Any = None
    operator: str
    citation: Dict[str, Any]
    reason: Optional[str] = None


class SchemeMatchResult(BaseModel):
    """Evaluated scheme outcome with full provenance and metadata."""
    model_config = ConfigDict(extra="ignore")

    scheme_id: str
    scheme_name: str
    ministry: str = ""
    description: str = ""
    benefit: str = ""
    application_url: str = ""
    tags: List[str] = Field(default_factory=list)
    documents_required: List[str] = Field(default_factory=list)
    overall_status: str  # ELIGIBLE | NOT_ELIGIBLE | INSUFFICIENT_DATA
    eligible: bool
    score: float
    passed_count: int
    failed_count: int
    missing_count: int
    criteria: List[CriterionMatchResult]
    citations: List[Dict[str, Any]]


class MatchResponse(BaseModel):
    """Aggregate response for scheme matching endpoint."""
    matches: List[SchemeMatchResult]
    total_evaluated: int
    eligible_count: int
