"""
Schemes and Matching route for CiviQ API.
Orchestrates profile matching against schemes via the deterministic evaluator.
"""

import json
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Request, status
from pydantic import ValidationError

from ai_engine.evaluator import evaluate_eligibility
from ..config import settings
from ..schemas import (
    CriterionMatchResult,
    MatchResponse,
    ProfileSchema,
    SchemeMatchResult,
)

router = APIRouter(tags=["schemes"])


def _load_canonical_schemes() -> List[Dict[str, Any]]:
    """Loads schemes from the canonical extracted JSON file."""
    if not settings.SCHEMES_FILE.exists():
        return []
    try:
        with open(settings.SCHEMES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


@router.post("/match")
async def match_schemes(request: Request) -> Dict[str, Any]:
    """
    Evaluates a user profile against government schemes.
    The evaluator (ai_engine.evaluator.evaluate_eligibility) is the sole authority for eligibility.
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Malformed JSON request body",
        )

    if not isinstance(body, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body must be a JSON object",
        )

    # 1. Resolve profile
    if "profile" in body:
        profile_input = body["profile"]
        schemes_input = body.get("schemes")
    else:
        profile_input = body
        schemes_input = None

    if not isinstance(profile_input, dict):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Profile must be a valid JSON object",
        )

    try:
        validated_profile = ProfileSchema.model_validate(profile_input)
        profile_dict = validated_profile.model_dump()
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ve.errors(),
        )

    # 2. Resolve schemes to evaluate
    schemes_to_evaluate: List[Dict[str, Any]] = []
    if schemes_input is not None:
        if not isinstance(schemes_input, list):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="'schemes' must be a list of scheme objects",
            )
        for idx, s in enumerate(schemes_input):
            if not isinstance(s, dict):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Scheme at index {idx} must be an object",
                )
            schemes_to_evaluate.append(s)
    else:
        schemes_to_evaluate = _load_canonical_schemes()

    # 3. Evaluate each scheme using evaluate_eligibility
    matches: List[Dict[str, Any]] = []

    for scheme in schemes_to_evaluate:
        try:
            eval_res = evaluate_eligibility(profile_dict, scheme)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Evaluator failed during scheme processing",
            )

        # Build criterion results preserving citations and metadata
        scheme_criteria = scheme.get("criteria", [])
        crit_by_id = {}
        for c in scheme_criteria:
            if isinstance(c, dict):
                crit_by_id[str(c.get("id"))] = c

        criteria_results: List[Dict[str, Any]] = []
        citations: List[Dict[str, Any]] = []

        for cr in eval_res.criteria:
            orig_crit = crit_by_id.get(str(cr.criterion_id), {})
            field_name = orig_crit.get("field", "")
            label_name = orig_crit.get("label", f"{field_name} {cr.operator} {cr.expected_value}")

            crit_dict = {
                "criterion_id": cr.criterion_id,
                "field": field_name,
                "label": label_name,
                "status": cr.status,
                "pass_status": (cr.status == "PASS"),
                "pass": (cr.status == "PASS"),
                "user_value": cr.user_value,
                "expected_value": cr.expected_value,
                "operator": cr.operator,
                "citation": cr.citation,
                "evidence": cr.citation,
                "reason": cr.reason,
            }
            criteria_results.append(crit_dict)
            if cr.citation:
                citations.append(cr.citation)

        total_criteria = len(scheme_criteria)
        score = round(eval_res.passed_count / total_criteria, 2) if total_criteria > 0 else 1.0

        scheme_id = scheme.get("id", scheme.get("scheme_id", eval_res.scheme_id))
        scheme_name = scheme.get("name", scheme.get("scheme_name", "Unknown Scheme"))

        match_item = {
            "scheme_id": scheme_id,
            "scheme_name": scheme_name,
            "ministry": scheme.get("ministry", ""),
            "description": scheme.get("short_desc", scheme.get("description", "")),
            "benefit": scheme.get("benefit_summary", scheme.get("benefit", "")),
            "application_url": scheme.get("application_url", ""),
            "tags": scheme.get("tags", []),
            "documents_required": scheme.get("documents_required", []),
            "overall_status": eval_res.overall_status,
            "eligible": (eval_res.overall_status == "ELIGIBLE"),
            "score": score,
            "passed_count": eval_res.passed_count,
            "failed_count": eval_res.failed_count,
            "missing_count": eval_res.missing_count,
            "criteria": criteria_results,
            "citations": citations,
        }
        matches.append(match_item)

    eligible_count = sum(1 for m in matches if m["eligible"])

    return {
        "matches": matches,
        "total_evaluated": len(matches),
        "eligible_count": eligible_count,
    }
