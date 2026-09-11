import os
import glob
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini once
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

CACHE_FILE = os.path.join(os.path.dirname(__file__), "uploaded_files.json")

def upload_all_pdfs(pdf_dir: str = "data/raw_pdfs") -> dict:
    """
    Scans the PDF folder and uploads all scheme guidelines to Gemini File API.
    Caches uploaded file metadata to avoid re-uploading.
    """
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")

    # Locate PDFs relative to repo root if path is relative
    if not os.path.isabs(pdf_dir):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        pdf_dir = os.path.join(base_dir, pdf_dir)

    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {pdf_dir}")
        return {}

    uploaded_files = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                uploaded_files = json.load(f)
        except Exception:
            uploaded_files = {}

    print(f"Checking {len(pdf_files)} PDFs for Gemini File API registration...")
    updated = False

    for file_path in pdf_files:
        filename = os.path.basename(file_path)
        
        # Check if already registered and valid
        if filename in uploaded_files:
            try:
                # Test if file still exists in Gemini
                remote_file = genai.get_file(uploaded_files[filename]["name"])
                if remote_file.state.name == "ACTIVE":
                    print(f"✓ Already active: {filename}")
                    continue
            except Exception:
                print(f"Re-uploading expired or missing file: {filename}")

        print(f"Uploading to Gemini File API: {filename}...")
        try:
            uploaded = genai.upload_file(path=file_path, display_name=filename)
            uploaded_files[filename] = {
                "name": uploaded.name,
                "uri": uploaded.uri,
                "display_name": filename,
                "size_bytes": uploaded.size_bytes
            }
            updated = True
            print(f"✓ Successfully uploaded: {filename} -> {uploaded.name}")
        except Exception as e:
            print(f"✗ Failed to upload {filename}: {e}")

    if updated or not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(uploaded_files, f, indent=2)

    return uploaded_files

def get_uploaded_files() -> list:
    """
    Returns active Gemini file handles for all registered scheme documents.
    """
    if not os.path.exists(CACHE_FILE):
        return []

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        handles = []
        for item in data.values():
            try:
                file_handle = genai.get_file(item["name"])
                handles.append(file_handle)
            except Exception as e:
                print(f"Warning: Could not fetch handle for {item['name']}: {e}")
        return handles
    except Exception as e:
        print(f"Error reading file cache: {e}")
        return []

if __name__ == "__main__":
    upload_all_pdfs()
