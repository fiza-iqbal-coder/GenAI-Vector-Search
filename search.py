import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from config import COLLECTION, DB_PATH, MODEL_NAME, TOP_K


def main() -> None:
    if not DB_PATH.exists():
        print("Database not found. Run: python ingest.py")
        return
    db = chromadb.PersistentClient(path=str(DB_PATH), settings=Settings(anonymized_telemetry=False))
    try:
        collection = db.get_collection(COLLECTION)
    except Exception:
        print("Collection not found. Run: python ingest.py")
        return
    if collection.count() == 0:
        print("Collection is empty. Run: python ingest.py")
        return
    model = SentenceTransformer(MODEL_NAME)
    print("Semantic search ready. Type 'exit' to quit.")
    while True:
        try:
            question = input("\nYour question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue
        vector = model.encode([question], normalize_embeddings=True).tolist()[0]
        results = collection.query(query_embeddings=[vector], n_results=min(TOP_K, collection.count()), include=["documents", "metadatas", "distances"])
        for rank, (doc, meta, distance) in enumerate(zip(results["documents"][0], results["metadatas"][0], results["distances"][0]), start=1):
            print(f"\n--- Result {rank} | source: {meta['source']} | chunk: {meta['chunk_index']} | cosine distance: {distance:.4f} ---")
            print(doc)


if __name__ == "__main__":
    main()
