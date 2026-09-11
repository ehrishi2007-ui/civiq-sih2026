import os
import google.generativeai as genai
from dotenv import load_dotenv
from backend.ai_engine.vector_store import get_uploaded_files

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Use the latest high-accuracy Gemini 2.5 Flash model
_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="""
You are CiviQ's Policy Intelligence AI.
Answer citizen questions strictly based on the attached official Indian government scheme guideline PDFs.

Format your answer clearly:
1. Direct Answer: A concise, empathetic, and clear explanation for the citizen.
2. Official Citation:
   - Document Name
   - Page Number
   - Exact Clause / Verbatim Quote
3. If the answer cannot be found in the attached documents, explicitly state:
   "The available official policy documents do not contain information regarding this."
4. Do NOT hallucinate rules or invent eligibility thresholds.
"""
)

def ask_policy(question: str) -> dict:
    """
    Queries Gemini 2.5 Flash using the long context of attached official PDFs.
    
    Args:
        question: User's query (e.g., 'What is the family income limit for PMSS?')
    
    Returns:
        Dictionary with answer text, model info, and status.
    """
    if not API_KEY:
        return {
            "success": False,
            "error": "GEMINI_API_KEY not configured",
            "answer": "API key is missing. Please check your backend .env configuration."
        }

    files = get_uploaded_files()
    if not files:
        return {
            "success": False,
            "error": "No documents loaded",
            "answer": "No scheme guideline PDFs are currently indexed in Gemini. Please run vector_store.py first."
        }

    try:
        # Pass all loaded PDFs + the user question into Gemini's multi-document context
        prompt_content = [*files, f"User Question: {question}"]
        response = _model.generate_content(prompt_content)

        return {
            "success": True,
            "answer": response.text,
            "documents_consulted": len(files),
            "model": "gemini-2.5-flash"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "answer": f"An error occurred while consulting policy documents: {e}"
        }

if __name__ == "__main__":
    test_q = "What is the scholarship amount for girls under PMSS?"
    print(f"Testing Question: {test_q}")
    res = ask_policy(test_q)
    print(res["answer"])
