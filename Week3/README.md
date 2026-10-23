# Week 3: Full RAG Pipeline

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline using Python, ChromaDB, Sentence Transformers, Google's Gemini API, and Rich.

The system retrieves relevant text chunks from a previously indexed document collection and uses them as context to answer user questions. It is designed to answer using the provided documents rather than relying on outside knowledge.

## Features

- Retrieves the top 3 relevant text chunks from ChromaDB.
- Uses Sentence Transformers to generate query embeddings.
- Builds a context string from retrieved document chunks.
- Generates context-grounded answers using Gemini.
- Displays retrieved sources and distances in a formatted terminal table.
- Includes source chunk citations in generated answers.
- Refuses unrelated questions when the retrieved results fail the configured distance threshold.
- Retries certain temporary API errors.
- Uses Rich for colored terminal output.

## Technologies Used

- Python
- ChromaDB
- Sentence Transformers
- Google Gemini API
- Python dotenv
- Rich

## Project Structure

```text
GenAI-Vector-Search/
├── rag_pipeline.py
├── ingest.py
├── sample_document.txt
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── chroma_db/
└── screenshots/
```

## Installation

### 1. Install dependencies

Open a terminal in the project directory and run:

```bash
python -m pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project directory.

Add the following settings:

```text
GEMINI_API_KEY=your_actual_api_key
GEMINI_MODEL=gemini-3.8-flash
```

Replace the placeholder with your own Gemini API key.

Do not upload `.env` or expose your API key publicly.

### 3. Verify the database

The project uses the existing ChromaDB collection:

`week2_documents`

The `chroma_db` directory must contain the database created during Week 2.

### 4. Run the pipeline

Execute:

```bash
python rag_pipeline.py
```

Enter a question when prompted. Type `exit` to close the application.

## How the Pipeline Works

1. The user enters a question.
2. Sentence Transformers converts the question into an embedding.
3. ChromaDB retrieves the three closest document chunks.
4. The retrieved chunks are displayed with their sources and distances.
5. The pipeline checks the closest retrieval distance against a configured threshold.
6. If the retrieved results pass the threshold, their text is combined into a context string.
7. Gemini generates an answer using the retrieved context.
8. The answer is displayed with source chunk citations.

If the closest retrieved chunk exceeds the configured distance threshold, the pipeline returns the refusal message without requesting an answer from Gemini.

## Testing

### Test 1: Relevant question

**Question:**

`what is machine learning`

**Observed result:**

The pipeline generated an answer explaining that machine learning algorithms learn patterns from examples rather than relying solely on hand-written rules.

The answer cited `[Chunk 1]`.

**Status:** Passed.

### Test 2: Unrelated question

**Question:**

`what is the capital of France`

**Expected and observed refusal:**

`I cannot find the answer in the provided documents.`

The closest retrieved distance was greater than the configured threshold of `0.85`.

**Status:** Passed.

## Screenshots

The `screenshots` directory contains evidence of the successful refusal test and screenshots of errors encountered during development.

- `refusal_test.png` — successful unrelated-question refusal.
- Additional screenshots — development errors and troubleshooting evidence.

Update these filenames if your saved screenshots use different names.

## Troubleshooting

During development, the following issues were encountered:

1. **Requirements installation:** The terminal initially pointed to the parent directory. Installation succeeded after navigating to the correct project folder.
2. **Gemini model error:** A `404 NOT_FOUND` error occurred for the initially configured model. The model setting was updated.
3. **Temporary API errors:** Gemini returned `503 UNAVAILABLE`. Retry handling with exponential backoff was added.
4. **Undefined function:** The call to `generate()` was corrected to `generate_answer()`.
5. **Missing prompt function:** The missing `build_prompt()` function was added.

See the screenshots directory for available error evidence.

## Limitations

- Answer quality depends on the indexed documents and the relevance of retrieved chunks.
- The retrieval-distance threshold is a preliminary filter and may require tuning.
- The prompt encourages context-only answers, but it does not guarantee that every generated answer will be factually correct.
- Gemini API availability and rate limits can affect response generation.

## Security

API credentials are stored in a local `.env` file and should not be committed to GitHub. The `.gitignore` file should exclude `.env` and other sensitive local files.

## Conclusion

This project integrates vector retrieval and a generative language model into a functional RAG pipeline. It retrieves relevant document chunks, generates cited answers, displays retrieval information, and demonstrates refusal behavior for an unrelated question.