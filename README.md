### Semantic Vector Search Engine

This project implements a multi-document embedding search engine with caching, as required by the assignment.
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

## 📸 Screenshots / Demo Output

<img width="428" height="536" alt="Screenshot 2025-11-21 130002" src="https://github.com/user-attachments/assets/53d19ffb-d3cb-48dc-9b05-bc4cde72cb42" />
<img width="402" height="561" alt="Screenshot 2025-11-21 130009" src="https://github.com/user-attachments/assets/a88cbac3-a614-4f49-84fe-d6d6f444f1a0" />
<img width="1906" height="887" alt="Screenshot 2025-11-21 190651" src="https://github.com/user-attachments/assets/8037c5bd-d9b0-47a3-9c73-e21ef5f2b5d5" />
<img width="1886" height="828" alt="Screenshot 2025-11-21 191204" src="https://github.com/user-attachments/assets/60cc5107-c1fc-4de3-8960-38d452324222" />
<img width="1871" height="888" alt="Screenshot 2025-11-21 191222" src="https://github.com/user-attachments/assets/2992b123-3962-4afd-8e1c-3f65f6b0bf46" />
<img width="1871" height="888" alt="Screenshot 2025-11-21 191222" src="https://github.com/user-attachments/assets/73a59c55-c76f-4abe-9ecd-50aca0613453" />

## Process (screenshots)

<img width="1128" height="565" alt="Screenshot 2025-11-21 125904" src="https://github.com/user-attachments/assets/baf33971-26dd-4be7-9ad8-02d41723571f" />
<img width="1532" height="992" alt="Screenshot 2025-11-21 125911" src="https://github.com/user-attachments/assets/1b7a23c1-68bf-4aa3-a89f-4c66da09fa97" />
<img width="1920" height="1080" alt="Screenshot 2025-11-21 125931" src="https://github.com/user-attachments/assets/7df3daf0-1368-4bf9-bf67-3c6940cfdebb" />
<img width="1123" height="616" alt="Screenshot 2025-11-21 130037" src="https://github.com/user-attachments/assets/e862f9fe-c2b3-4e48-8a77-0385628a878f" />
<img width="1127" height="837" alt="Screenshot 2025-11-21 130254" src="https://github.com/user-attachments/assets/6059a87f-a0f3-40f1-85ef-df6545b0278b" />
<img width="1110" height="868" alt="Screenshot 2025-11-21 130353" src="https://github.com/user-attachments/assets/723bd202-762f-487e-b8ec-600429c8079a" />




