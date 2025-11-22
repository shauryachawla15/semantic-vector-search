Semantic Vector Search Engine

A modular semantic search system built using Python, FastAPI, and Sentence-Transformers.
This project demonstrates:

Generating embeddings for text documents

Caching embeddings to avoid recomputation

Performing vector search using cosine similarity

Exposing a search API for retrieval

Providing ranking explanations for results

📁 Project Structure
project/
│
├── data/               # ignored in Git
│   └── docs/           # dataset text files
│
├── src/
│   ├── embedder.py
│   ├── embedding_model.py
│   ├── cache_manager.py
│   ├── search_engine.py
│   ├── api.py
│   └── __init__.py
│
├── README.md
├── requirements.txt
└── .gitignore

⚡ How Caching Works

We use a simple JSON file (embedding_cache.json) to store embeddings.

Each entry looks like:

{
  "doc_id": "doc_001",
  "embedding": [...384-dimensional vector...],
  "hash": "sha256_text_hash",
  "updated_at": 1732138217.221
}

Caching Logic

Read document

Clean text (lowercase, remove HTML, trim spaces)

Compute SHA-256 hash

Compare hash with cached version

If same → load cached embedding

If different → compute new embedding and update cache

This makes search extremely fast since embeddings don't need to be recomputed.

📥 Downloading the Dataset

Use the provided script:

python download_dataset.py


This creates:

data/docs/doc_0000.txt ... doc_0199.txt


(These files are ignored in GitHub via .gitignore)

🧠 Embedding Pipeline

To test embedding generation:

cd src
python test_embedding.py


You should see logs like:

Loading embedding model: all-MiniLM-L6-v2
Embedding shape: (384,)

🚀 Starting the Search API

Run the FastAPI server:

cd src
uvicorn api:app --reload --host 127.0.0.1 --port 8000


API docs open at:

👉 http://127.0.0.1:8000/docs

🔍 Running a Search Query

Example request:

POST /search


Body:

{
  "query": "machine learning algorithms",
  "top_k": 5
}


Response:

{
  "results": [
    ["doc_0153", 0.42],
    ["doc_0059", 0.40],
    ["doc_0049", 0.28]
  ]
}

📊 Ranking Explanation

Each search result includes (if enabled):

doc_id – which document matched

score – cosine similarity

reason – simple keyword overlap check

overlap_ratio – heuristic scoring

length_norm – optional length-normalized score

This helps understand why the model picked a document.

🏗️ Design Choices
Embedding Model

sentence-transformers/all-MiniLM-L6-v2

Small, fast, accurate for semantic vector search

Cache

Simple JSON-based storage

Easy to inspect, portable, reliable

Search Engine

Pure NumPy cosine similarity

Simple and transparent

API

FastAPI for clean automatic documentation

Pydantic validation

📦 Installation
pip install -r requirements.txt

▶️ Full Run Instructions
python download_dataset.py
cd src
python test_embedding.py
uvicorn api:app --reload


Then visit:

👉 http://127.0.0.1:8000/docs

🎯 Optional Improvements (Bonus Ideas)

Streamlit UI

FAISS index

Query expansion using WordNet

Multiprocessing for batch embeddings

Quality evaluation with test queries