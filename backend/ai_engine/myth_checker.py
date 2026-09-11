import os
import json
from typing import Any, Dict, List

MYTHS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "myths.json"))

def load_myths() -> List[Dict[str, Any]]:
    """Loads curated fake scheme claims and verified facts."""
    if not os.path.exists(MYTHS_FILE):
        return []
    try:
        with open(MYTHS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading myths.json: {e}")
        return []

def check_myth(query: str) -> Dict[str, Any]:
    """
    Checks user inquiry or WhatsApp forward claim against curated fake scheme registry.
    """
    myths = load_myths()
    query_clean = query.lower().strip()

    for item in myths:
        keywords = item.get("claim_keywords", [])
        # Match keywords in query
        for kw in keywords:
            if kw.lower() in query_clean:
                return {
                    "verdict": item.get("verdict", "FAKE"),
                    "warning": item.get("warning", "No such government scheme exists. Beware of fraudulent links."),
                    "real_scheme": item.get("real_scheme_name", ""),
                    "real_facts": item.get("real_facts", ""),
                    "citation": item.get("citation", "Official Gazette Guidelines")
                }

    # Default response if no direct myth match is found
    return {
        "verdict": "UNVERIFIED",
        "warning": "This claim is not registered in our verified fact-check database. Always verify URLs end in .gov.in or .nic.in before sharing sensitive information.",
        "real_scheme": "General Advisory",
        "real_facts": "Government schemes are never disbursed via unverified WhatsApp links or third-party APKs.",
        "citation": "PIB Fact Check & National Cyber Crime Reporting Portal"
    }
