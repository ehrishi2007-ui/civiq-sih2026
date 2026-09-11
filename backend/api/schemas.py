"""
API Request and Response Pydantic Schemas for CiviQ.
"""

from typing import Any, Dict, List, Optional, Union
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
    marks_percentage: Optional[float] = Field(default=None, ge=0, le=100, description="Marks percentage in qualifying examination (MEQ)")


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


class AskRequest(BaseModel):
    """Citizen query request for policy intelligence."""
    model_config = ConfigDict(extra="allow")

    question: str = Field(..., min_length=1, description="Question about government policies or schemes")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional conversational or profile context")


class SourceCitation(BaseModel):
    """Grounded source citation from official scheme document."""
    model_config = ConfigDict(extra="allow")

    document: Optional[str] = None
    doc_name: Optional[str] = None
    page: Optional[int] = None
    section: Optional[str] = None
    quote: Optional[str] = None


class AskResponse(BaseModel):
    """Response contract for policy intelligence and Ask CiviQ AI."""
    model_config = ConfigDict(extra="allow")

    answer: str
    sources: List[Union[SourceCitation, Dict[str, Any]]] = Field(default_factory=list)


class MythCheckRequest(BaseModel):
    """Citizen inquiry or claim text to verify against misinformation."""
    model_config = ConfigDict(extra="allow")

    claim: str = Field(..., min_length=1, description="Government scheme claim, rumor, or forward to fact-check")


class MythSource(BaseModel):
    """Grounded official source citation for myth verification."""
    model_config = ConfigDict(extra="allow")

    document: Optional[str] = None
    doc_name: Optional[str] = None
    page: Optional[int] = None
    section: Optional[str] = None
    quote: Optional[str] = None


class MythCheckResponse(BaseModel):
    """Fact-check verification result conforming to CiviQ frontend contract."""
    model_config = ConfigDict(extra="allow")

    verdict: str = Field(..., description="Fact-check verdict: TRUE | FALSE | PARTIALLY TRUE | UNVERIFIED")
    explanation: str = Field(..., description="Factual explanation clarifying the claim")
    sources: List[Union[MythSource, Dict[str, Any]]] = Field(default_factory=list, description="Grounded official document citations")
    warning: Optional[str] = None
    real_scheme: Optional[str] = None
    real_facts: Optional[str] = None
    citation: Optional[str] = None


class ComparatorRequest(BaseModel):
    """Request payload for scheme policy version comparison."""
    model_config = ConfigDict(extra="allow")

    scheme_id: str = Field(default="pm_scholarship_warb", description="Scheme identifier to compare")
    user_profile: Optional[Dict[str, Any]] = Field(default=None, description="Optional citizen profile to assess eligibility impact")


class PolicyChangeItem(BaseModel):
    """Individual policy parameter difference."""
    model_config = ConfigDict(extra="allow")

    field: str
    param: Optional[str] = None
    old_value: str
    old_val: Optional[str] = None
    new_value: str
    new_val: Optional[str] = None
    change_label: Optional[str] = None
    change: Optional[str] = None
    direction: Optional[str] = "neutral"
    impact: Optional[str] = None
    sources: List[Dict[str, Any]] = Field(default_factory=list)


class ComparatorResponse(BaseModel):
    """Policy comparison response for CiviQ."""
    model_config = ConfigDict(extra="allow")

    scheme_id: str
    scheme_name: str
    old_version: str = "2023-24"
    new_version: str = "2026-27"
    version_old: Optional[str] = "2023-24"
    version_new: Optional[str] = "2026-27"
    verified: bool = False
    status: str = "UNVERIFIED_NEW_VERSION"
    message: str
    changes: List[PolicyChangeItem] = Field(default_factory=list)
    diff_matrix: List[Dict[str, Any]] = Field(default_factory=list)
    personalized_impact: Optional[str] = None
    sources: List[Dict[str, Any]] = Field(default_factory=list)


class TranslateRequest(BaseModel):
    """Citizen request payload for UI or dynamic text translation."""
    model_config = ConfigDict(extra="allow")

    text: str = Field(..., description="Text content to translate")
    target_language: str = Field(..., min_length=2, description="ISO 639-1 code of target language")


class TranslateResponse(BaseModel):
    """Response payload conforming to CiviQ frontend translation contract."""
    model_config = ConfigDict(extra="allow")

    translated_text: str = Field(..., description="Translated or fallback string")
    target_language: str = Field(..., description="Target language code")
    detected_source_language: str = Field(default="en", description="Detected or default source language code")

