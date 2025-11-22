import numpy as np
import glob
import os
from embedding_model import EmbeddingModel
from cache_manager import CacheManager
from embedder import load_document


def cosine_similarity(a, b):
    """Compute cosine similarity between vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class SearchEngine:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.cache = CacheManager()

        print("[INIT] Loading document embeddings...")

        # Load all docs
        self.docs = sorted(glob.glob("../data/docs/*.txt"))

        # Load (or compute) embeddings
        self.embeddings, self.doc_ids = self.load_all_embeddings()

    def embed_query(self, query: str):
        """Embed a search query."""
        return self.embedder.model.encode(query)

    def load_all_embeddings(self):
        """Load embeddings for all documents from cache or compute fresh."""
        embeddings = []
        doc_ids = []

        for doc_path in self.docs:
            doc_id = os.path.basename(doc_path).replace(".txt", "")

            # Load document metadata (text + hash)
            doc = load_document(doc_path)
            doc_hash = doc["hash"]

            # Try cache
            cached = self.cache.get_cached(doc_id, doc_hash)

            if cached is not None:
                emb = np.array(cached)
            else:
                emb = self.embedder.embed_document(doc_path, doc_id)

            embeddings.append(emb)
            doc_ids.append(doc_id)

        return np.array(embeddings), doc_ids

    def search(self, query: str, top_k=5):
        """Perform semantic vector search."""
        print("\n🔍 Running Semantic Search...")

        query_emb = self.embed_query(query)

        sims = []

        for i, emb in enumerate(self.embeddings):
            sim = cosine_similarity(query_emb, emb)
            sims.append((self.doc_ids[i], sim))

        sims.sort(key=lambda x: x[1], reverse=True)

        return sims[:top_k]
