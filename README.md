# GenAI-Vector-Search

Week 2 internship project: chunk a plain-text document, generate local embeddings, store them in ChromaDB, and retrieve the top 3 semantically relevant chunks.

## Stack
- Python 3.10+
- `sentence-transformers/all-MiniLM-L6-v2` (local embeddings; 384 dimensions)
- ChromaDB persistent local vector store with cosine distance

## Setup (Windows PowerShell)
```powershell
cd GenAI-Vector-Search
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
If `py -3.10` is unavailable, use `python -m venv .venv` with a supported Python installation. If PowerShell blocks activation, use `.venv\Scripts\python.exe` directly instead of activating.

## Run
```powershell
python ingest.py
python search.py
```
The first run downloads the embedding model (internet required). The database is saved in `chroma_db/` and persists between runs.

To index another UTF-8 text file:
```powershell
python ingest.py --file "data/my_document.txt"
```
The sample is deliberately short, so the final chunk may have fewer than 200 words. Long sentences are split at word boundaries if necessary.

## Pipeline
Text file -> sentence-aware chunks (target 200-250 words) -> local embedding vectors -> ChromaDB -> user query embedded with same model -> top 3 chunks.

## Try these questions
- How can I find related passages when they use different words?
- Where are numerical representations of documents stored?
- Why should I keep the embedding model consistent?

## Files
- `config.py`: shared model and storage settings
- `chunking.py`: sentence-aware text splitting
- `ingest.py`: read, chunk, embed, and persist
- `search.py`: interactive semantic search
- `data/sample_document.txt`: example input
- `TROUBLESHOOTING.md`: issues and fixes
- `.gitignore`: excludes secrets, virtual environments, and generated database

## GitHub submission
Create a new public or private repository named `GenAI-Vector-Search`, then run:
```powershell
git init
git add .
git commit -m "Build local semantic vector search"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```
Never commit `.env` or credentials. `.env.example` is safe to commit.

## Notes
- Retrieval prints original passages, not LLM-generated answers.
- Cosine **distance** is displayed: lower is better.
- Re-ingesting the same absolute file path replaces its previous chunks.
- The code is provided as a ready-to-run starter project; run it locally and record your real testing results before submission.
