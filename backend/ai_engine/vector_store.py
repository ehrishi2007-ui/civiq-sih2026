import os
import glob
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

CACHE_FILE = os.path.join(os.path.dirname(__file__), "uploaded_files.json")

def upload_all_pdfs(pdf_dir: str = "data/raw_pdfs") -> dict:
    """
    Scans the PDF folder and uploads all scheme guidelines to Gemini File API using google-genai SDK.
    Caches uploaded file metadata to avoid re-uploading.
    """
    if not client:
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
                remote_file = client.files.get(name=uploaded_files[filename]["name"])
                if remote_file.state.name == "ACTIVE":
                    print(f"Already active in Gemini: {filename}")
                    continue
            except Exception:
                print(f"Re-uploading: {filename}")

        print(f"Uploading to Gemini File API: {filename}...")
        try:
            uploaded = client.files.upload(file=file_path)
            uploaded_files[filename] = {
                "name": uploaded.name,
                "uri": uploaded.uri,
                "display_name": filename,
                "size_bytes": getattr(uploaded, "size_bytes", None)
            }
            updated = True
            print(f"Successfully uploaded: {filename} -> {uploaded.name}")
        except Exception as e:
            print(f"Failed to upload {filename}: {e}")

    # Prune any cached entries for files that no longer exist on disk
    current_filenames = {os.path.basename(p) for p in pdf_files}
    stale_files = [fn for fn in uploaded_files if fn not in current_filenames]
    for fn in stale_files:
        print(f"Removing stale cached entry: {fn}")
        del uploaded_files[fn]
        updated = True

    if updated or not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(uploaded_files, f, indent=2)

    print(f"Gemini PDF Document Registry is ready! ({len(uploaded_files)} documents active)")
    return uploaded_files

def get_uploaded_files() -> list:
    """
    Returns active Gemini file handles for all registered scheme documents.
    """
    if not client or not os.path.exists(CACHE_FILE):
        return []

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        handles = []
        for item in data.values():
            try:
                file_handle = client.files.get(name=item["name"])
                handles.append(file_handle)
            except Exception as e:
                print(f"Warning: Could not fetch handle for {item['name']}: {e}")
        return handles
    except Exception as e:
        print(f"Error reading file cache: {e}")
        return []

if __name__ == "__main__":
    upload_all_pdfs()
