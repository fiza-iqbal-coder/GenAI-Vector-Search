import argparse
import hashlib

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from chunking import chunk_text
from config import CHUNK_WORDS, COLLECTION, DB_PATH, DOCUMENT, MIN_CHUNK_WORDS, MODEL_NAME


def main() -> None:
    parser = argparse.ArgumentParser(description="Embed a text file into local ChromaDB")
    parser.add_argument("--file", default=str(DOCUMENT), help="Path to UTF-8 text file")
    args = parser.parse_args()

    from pathlib import Path
    source = Path(args.file).resolve()
    text = source.read_text(encoding="utf-8")
    chunks = chunk_text(text, CHUNK_WORDS, MIN_CHUNK_WORDS)
    if not chunks:
        raise ValueError("The document is empty.")

    print(f"Loaded {source.name}; generated {len(chunks)} chunks.")
    model = SentenceTransformer(MODEL_NAME)
    vectors = model.encode(chunks, normalize_embeddings=True, show_progress_bar=True).tolist()
    db = chromadb.PersistentClient(path=str(DB_PATH), settings=Settings(anonymized_telemetry=False))
    collection = db.get_or_create_collection(name=COLLECTION, metadata={"hnsw:space": "cosine"})

    # Re-ingesting the same file updates its chunks without duplicating them.
    source_id = hashlib.sha256(str(source).encode("utf-8")).hexdigest()[:16]
    old = collection.get(where={"source_id": source_id})
    if old["ids"]:
        collection.delete(ids=old["ids"])
    ids = [f"{source_id}-{i}" for i in range(len(chunks))]
    collection.add(
        ids=ids,
        embeddings=vectors,
        documents=chunks,
        metadatas=[{"source": source.name, "source_id": source_id, "chunk_index": i} for i in range(len(chunks))],
    )
    print(f"Saved {len(chunks)} chunks to {DB_PATH}. Collection: {COLLECTION}")


if __name__ == "__main__":
    main()
