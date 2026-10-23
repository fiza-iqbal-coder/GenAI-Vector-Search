from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCUMENT = ROOT / "data" / "sample_document.txt"
DB_PATH = ROOT / "chroma_db"
COLLECTION = "week2_documents"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_WORDS = 250
MIN_CHUNK_WORDS = 200
TOP_K = 3
