"""
CiviQ M5 - Policy Intelligence & Grounded Document RAG Service.

Responsible for:
1. Grounded policy Q&A using official government scheme PDFs.
2. Interfacing with Google Gemini via the official modern google-genai SDK.
3. Distinguishing information explicitly established in official documents vs unverified.
4. Extracting structured citations without fabricating page numbers.
5. Strict architectural boundary: RAG never calculates or overrides citizen eligibility.
"""

import json
import os
import re
from typing import Any, Dict, List, Optional

from google import genai
from google.genai import types

try:
    from api.config import settings
except ImportError:
    from backend.api.config import settings

try:
    from .pdf_service import (
        GeminiAuthError,
        get_gemini_client,
        get_official_pdf_handles,
    )
except ImportError:
    from ai_engine.pdf_service import (
        GeminiAuthError,
        get_gemini_client,
        get_official_pdf_handles,
    )


SYSTEM_INSTRUCTION = """You are CiviQ's Policy Intelligence AI.
Answer citizen questions strictly based on the attached official Indian government scheme guideline PDFs.

Guidelines:
1. Direct Answer: Provide a concise, empathetic, and clear explanation for the citizen.
2. Official Citation: Cite the official source whenever establishing a rule:
   - Document Name (e.g. PM-KISAN.pdf, PMEGP.pdf, PMSS 2023-24.pdf, StandupIndia.pdf)
   - Page Number
   - Exact Clause / Verbatim Quote
3. If the answer cannot be established from the supplied documents, explicitly state:
   "The available official policy documents do not contain information regarding this."
4. Distinguish clearly between:
   - Information explicitly supported by the official documents.
   - Information that cannot be established from the official documents.
5. Do NOT hallucinate rules, fabricate citations, or invent eligibility criteria.
6. Crucial boundary: Never calculate or override deterministic citizen eligibility. Scheme eligibility calculations are handled exclusively by CiviQ's deterministic engine.
"""

# Known approved documents for citation extraction
KNOWN_DOCUMENTS = {
    "PM-KISAN.pdf",
    "PMEGP.pdf",
    "PMSS 2023-24.pdf",
    "PMSS 2026-27.pdf",
    "StandupIndia.pdf",
    "APY.pdf",
}


def extract_citations(text: str) -> List[Dict[str, Any]]:
    """
    Extracts structured citation objects from model response text.
    Strictly avoids fabricating page numbers or citations if absent from model output.
    """
    if not text:
        return []

    citations: List[Dict[str, Any]] = []
    seen_keys = set()

    # Pattern 1: Structured bullet / block format
    # Matches patterns like:
    # Document Name: PM-KISAN.pdf
    # Page Number: 2
    # Clause / Quote: "..."
    block_pattern = re.compile(
        r"(?:Document(?:\s*Name)?|Doc):\s*([A-Za-z0-9_\-\. ]+\.pdf)"
        r"(?:[^\n\r]*\n[^\n\r]*Page(?:\s*(?:Number|No\.?))?:\s*(\d+))?"
        r"(?:[^\n\r]*\n[^\n\r]*(?:Exact\s+Clause|Clause|Quote|Verbatim Quote):\s*[\"']?([^\"\n\r]+)[\"']?)?",
        re.IGNORECASE,
    )

    for match in block_pattern.finditer(text):
        doc_name = match.group(1).strip()
        page_str = match.group(2)
        quote_str = match.group(3)

        page_num = int(page_str) if page_str else None
        quote = quote_str.strip() if quote_str else None

        key = (doc_name, page_num)
        if key not in seen_keys:
            seen_keys.add(key)
            citations.append({
                "document": doc_name,
                "doc_name": doc_name,
                "page": page_num,
                "section": None,
                "quote": quote,
            })

    # Pattern 2: Inline document mention fallback if block pattern didn't match
    if not citations:
        for doc in sorted(KNOWN_DOCUMENTS):
            if doc.lower() in text.lower():
                # Check for adjacent page number if explicitly written, e.g. "PM-KISAN.pdf (page 2)"
                page_match = re.search(
                    re.escape(doc) + r"[^\n\r]{0,30}?(?:page|pg\.?)\s*(\d+)",
                    text,
                    re.IGNORECASE,
                )
                page_num = int(page_match.group(1)) if page_match else None
                key = (doc, page_num)
                if key not in seen_keys:
                    seen_keys.add(key)
                    citations.append({
                        "document": doc,
                        "doc_name": doc,
                        "page": page_num,
                        "section": None,
                        "quote": None,
                    })

    return citations


def ask_policy(
    question: str,
    context: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Queries Gemini using long-context official policy document handles.
    
    Returns a dictionary conforming to the frontend contract:
    {
        "answer": str,
        "sources": List[Dict[str, Any]],
        "success": bool,
        "documents_consulted": int,
        "model": str,
    }
    """
    if not question or not question.strip():
        return {
            "answer": "Please provide a valid question regarding government schemes or policies.",
            "sources": [],
            "success": False,
            "error": "Empty question",
        }

    resolved_api_key = api_key or os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY
    if not resolved_api_key or not resolved_api_key.strip():
        return {
            "answer": "GEMINI_API_KEY is not configured. Please configure your API key to query official policy documents.",
            "sources": [],
            "success": False,
            "error": "GEMINI_API_KEY not configured",
        }

    try:
        client = get_gemini_client(api_key=resolved_api_key)
    except GeminiAuthError as e:
        return {
            "answer": str(e),
            "sources": [],
            "success": False,
            "error": str(e),
        }

    try:
        handles_dict = get_official_pdf_handles(api_key=resolved_api_key)
    except Exception as e:
        return {
            "answer": f"Could not load official policy documents: {str(e)}",
            "sources": [],
            "success": False,
            "error": str(e),
        }

    if not handles_dict:
        return {
            "answer": "No official policy documents are currently indexed in Gemini. Please run document ingestion first.",
            "sources": [],
            "success": False,
            "error": "No documents loaded",
        }

    # Fetch active File handles from Gemini File API
    file_objects = []
    for doc_name, info in sorted(handles_dict.items()):
        gemini_name = info.get("gemini_name")
        if gemini_name:
            try:
                f_obj = client.files.get(name=gemini_name)
                file_objects.append(f_obj)
            except Exception:
                pass

    if not file_objects:
        return {
            "answer": "Could not access registered document handles from Gemini. Please verify Gemini File API credentials.",
            "sources": [],
            "success": False,
            "error": "No accessible file objects",
        }

    model_name = model or settings.GEMINI_MODEL

    # Construct prompt with optional context
    prompt_text = f"Citizen Question: {question.strip()}"
    if context:
        prompt_text = f"Citizen Context: {json.dumps(context)}\n\n{prompt_text}"

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[*file_objects, prompt_text],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2,
            ),
        )

        answer_text = response.text or ""
        sources = extract_citations(answer_text)

        return {
            "answer": answer_text,
            "sources": sources,
            "success": True,
            "documents_consulted": len(file_objects),
            "model": model_name,
        }
    except Exception as e:
        return {
            "answer": f"An error occurred while consulting policy documents: {str(e)}",
            "sources": [],
            "success": False,
            "error": str(e),
        }


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    test_q = "What is the scholarship amount for girls under PMSS?"
    print(f"Testing Question: {test_q}")
    res = ask_policy(test_q)
    print("\n--- POLICY ANSWER ---")
    print(res.get("answer"))
    print("\n--- SOURCES ---")
    print(res.get("sources"))
