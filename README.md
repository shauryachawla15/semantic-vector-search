### Semantic Vector Search Engine

A fully modular semantic search system built using:

1) Python
2) Sentence-Transformers (all-MiniLM-L6-v2)
3) FastAPI
4) Custom caching system
5) Cosine-similarity ranking

## 📁 Project Structure

```text
project/
│
├── data/               # ignored in Git (contains docs)
│   └── docs/           # dataset text files
│
├── src/
│   ├── embedder.py         # text cleaning + hashing utilities
│   ├── embedding_model.py  # loads embedding model + computes embeddings
│   ├── cache_manager.py    # stores & retrieves embeddings using JSON cache
│   ├── search_engine.py    # performs semantic search + ranking
│   ├── api.py              # FastAPI /search endpoint
│   └── __init__.py
│
├── README.md
├── requirements.txt
└── .gitignore
```


### How Caching Works

Every document is cleaned, hashed, and checked against a JSON cache:
{
  "doc_id": "doc_001",
  "embedding": [...],
  "hash": "sha256_hash_of_text",
  "updated_at": 1732164210.12
}

### When a document loads:

If hash matches → reuse stored embedding
If hash changed → re-embed and update cache

This makes the system fast and avoids recomputing 200+ embeddings

### Search Pipeline

When a user sends a query:

1) Query is embedded using all-MiniLM-L6-v2
2) All document embeddings are loaded (from cache or computed)
3) Cosine similarity is calculated between query + each doc
4) Top-K ranked documents are returned

Example API input:
{
  "query": "space shuttle engineering",
  "top_k": 5
}

Example API output:
{
  "results": [
    ["doc_0153", 0.42],
    ["doc_0059", 0.40],
    ["doc_0049", 0.28]
  ]
}

### Run the API
cd src
uvicorn api:app --reload --host 127.0.0.1 --port 8000

Visit:

📌 http://127.0.0.1:8000/docs
to test the /search endpoint.


### Design Choices

Sentence-Transformers chosen for fast CPU-friendly embeddings
JSON cache for transparency & simplicity
Custom cosine-similarity search (easy to understand & debug)
Modular src/ layout enables upgrading to:
    FAISS index
    Streamlit UI
    Batch embedding
    Query expansion



