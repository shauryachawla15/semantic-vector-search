import numpy as np
from src.embedder import clean_text, load_document
from src.cache_manager import CacheManager


class EmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.cache = CacheManager()

    def embed_document(self, doc_path: str, doc_id: str):
        """
        Loads, cleans, hashes, embeds, caches a document.
        """

        # 1. Load & clean text
        doc = load_document(doc_path)
        text = doc["text"]
        doc_hash = doc["hash"]

        # 2. Try retrieving from cache
        cached = self.cache.get_cached(doc_id, doc_hash)
        if cached is not None:
            print(f"[CACHE] Using cached embedding for {doc_id}")
            return np.array(cached)

        # 3. Embed fresh
        print(f"[EMBED] Computing embedding for {doc_id}")
        embedding = self.model.encode(text)

        # 4. Save to cache
        self.cache.update_cache(doc_id, doc_hash, embedding)

        return embedding
