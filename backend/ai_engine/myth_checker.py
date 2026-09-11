"""
CiviQ M6 - Curated Myth Buster & Misinformation Checker.

Responsible for:
1. Matching user scheme claims or WhatsApp rumors against verified curated registry.
2. Normalizing text (casing, punctuation, currency symbols, numerical formats).
3. Mapping verdicts to canonical frontend values (TRUE, FALSE, PARTIALLY TRUE, UNVERIFIED).
   - Adapts Dev1 "FAKE" -> "FALSE".
4. Returning grounded explanations and structured source citations.
5. Handling unknown claims conservatively as "UNVERIFIED" without guessing.
6. Strict architectural boundary: Myth Buster never evaluates citizen eligibility.
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from api.config import settings
except ImportError:
    from backend.api.config import settings


def _resolve_myths_file() -> Path:
    """Resolves path to data/myths.json safely."""
    if hasattr(settings, "MYTHS_FILE") and settings.MYTHS_FILE.exists():
        return settings.MYTHS_FILE
    base_dir = Path(__file__).resolve().parent.parent.parent
    return base_dir / "data" / "myths.json"


def load_myths(file_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Loads curated scheme claims and verified facts from disk."""
    target_path = file_path or _resolve_myths_file()
    if not target_path.exists():
        return []
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def normalize_query(text: str) -> str:
    """
    Normalizes claim query for resilient matching:
    - Lowercases
    - Normalizes Indian currency symbols ('₹', 'rs.', 'rs', 'rupees')
    - Removes punctuation and commas from numbers (e.g. '50,000' -> '50000')
    - Collapses excess whitespace
    """
    if not text:
        return ""
    
    cleaned = text.lower().strip()
    # Normalize currency representations
    cleaned = cleaned.replace("₹", "rs ")
    cleaned = re.sub(r"\brs\.?\b", "rs", cleaned)
    cleaned = re.sub(r"\brupees\b", "rs", cleaned)
    
    # Remove commas between digits (e.g., 50,000 -> 50000)
    cleaned = re.sub(r"(\d+),(\d+)", r"\1\2", cleaned)
    
    # Remove standard punctuation
    cleaned = re.sub(r"[\.,!?;:\"\'\(\)\[\]\{\}\-_/]", " ", cleaned)
    
    # Collapse multiple whitespaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def map_verdict(raw_verdict: Optional[str]) -> str:
    """
    Maps verdicts to canonical frontend contract:
    - 'FAKE' -> 'FALSE'
    - 'FALSE' -> 'FALSE'
    - 'TRUE' -> 'TRUE'
    - 'PARTIALLY TRUE' -> 'PARTIALLY TRUE'
    - Default / Unknown -> 'UNVERIFIED'
    """
    if not raw_verdict:
        return "UNVERIFIED"
    
    v = raw_verdict.strip().upper()
    if v in {"FAKE", "FALSE"}:
        return "FALSE"
    if v == "TRUE":
        return "TRUE"
    if v in {"PARTIALLY TRUE", "PARTIAL", "PARTIALLY_TRUE"}:
        return "PARTIALLY TRUE"
    return "UNVERIFIED"


def check_myth(query: str, myths_file: Optional[Path] = None) -> Dict[str, Any]:
    """
    Checks user inquiry or rumor against curated scheme registry.
    Returns response strictly conforming to frontend contract:
    {
        "verdict": "FALSE" | "TRUE" | "PARTIALLY TRUE" | "UNVERIFIED",
        "explanation": str,
        "sources": List[Dict[str, Any]],
        "warning": Optional[str],
        "real_scheme": Optional[str],
        "real_facts": Optional[str],
        "citation": Optional[str],
    }
    """
    if not query or not query.strip():
        return {
            "verdict": "UNVERIFIED",
            "explanation": "Please provide a valid claim to check.",
            "sources": [],
            "warning": "No claim provided.",
            "real_scheme": None,
            "real_facts": None,
            "citation": None,
        }

    myths = load_myths(myths_file)
    normalized_q = normalize_query(query)
    raw_clean_q = query.lower().strip()

    for item in myths:
        keywords = item.get("claim_keywords", [])
        matched = False

        for kw in keywords:
            kw_raw = kw.lower().strip()
            kw_norm = normalize_query(kw)

            # Match either raw query or normalized query
            if kw_raw in raw_clean_q or (kw_norm and kw_norm in normalized_q):
                matched = True
                break

        if matched:
            raw_verdict = item.get("verdict", "FALSE")
            verdict = map_verdict(raw_verdict)
            warning = item.get("warning", "No such government scheme exists. Beware of fraudulent links.")
            real_facts = item.get("real_facts", "")
            real_scheme = item.get("real_scheme_name", item.get("real_scheme", ""))
            
            # Prefer explicit explanation field; fallback to warning + real_facts
            explanation = item.get("explanation")
            if not explanation:
                explanation = f"{warning} {real_facts}".strip()

            # Structured sources list
            raw_sources = item.get("sources", [])
            structured_sources = []
            for src in raw_sources:
                if isinstance(src, dict):
                    doc_name = src.get("doc_name") or src.get("document")
                    structured_sources.append({
                        "document": doc_name,
                        "doc_name": doc_name,
                        "page": src.get("page"),
                        "section": src.get("section"),
                        "quote": src.get("quote"),
                    })

            return {
                "verdict": verdict,
                "explanation": explanation,
                "sources": structured_sources,
                "warning": warning,
                "real_scheme": real_scheme,
                "real_facts": real_facts,
                "citation": item.get("citation"),
            }

    # Default conservative response if no curated pattern matches
    return {
        "verdict": "UNVERIFIED",
        "explanation": (
            "This claim is not registered in our verified fact-check database. "
            "Always verify government schemes on official portals ending in .gov.in or .nic.in "
            "before sharing sensitive information or personal documents."
        ),
        "sources": [],
        "warning": (
            "This claim is not registered in our verified fact-check database. "
            "Always verify URLs end in .gov.in or .nic.in before sharing sensitive information."
        ),
        "real_scheme": "General Advisory",
        "real_facts": "Government benefits are never disbursed via unverified WhatsApp links or third-party APKs.",
        "citation": "PIB Fact Check & National Cyber Crime Reporting Portal",
    }


if __name__ == "__main__":
    test_claim = "Modi 50000 cash to farmers"
    res = check_myth(test_claim)
    print(f"Claim: {test_claim}")
    print(f"Verdict: {res['verdict']}")
    print(f"Explanation: {res['explanation']}")
    print(f"Sources: {res['sources']}")
