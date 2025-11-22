import json
import os
import time

CACHE_PATH = "embedding_cache.json"

class CacheManager:
    def __init__(self, cache_path=CACHE_PATH):
        # Path where we store all precomputed embeddings
        self.cache_path = cache_path
        
        # Load existing cache from file (or start empty)
        self.cache = self._load_cache()

    def _load_cache(self):
        """
        Load the cache from disk.
        If no cache file exists, return an empty dictionary.
        """
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_cache(self):
        """
        Write the current cache dictionary to disk as a JSON file.
        """
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2)

    def get_cached(self, doc_id: str, doc_hash: str):
        """
        Fetch an embedding from the cache.

        We only return the cached embedding if:
        - the document exists in the cache, AND
        - the saved hash matches the current hash of the document

        This ensures we never use an outdated embedding.
        """
        if doc_id in self.cache:
            entry = self.cache[doc_id]
            if entry["hash"] == doc_hash:
                return entry["embedding"]
        return None

    def update_cache(self, doc_id: str, doc_hash: str, embedding):
        """
        Save a new embedding into the cache along with:
        - the document hash (to detect changes)
        - the timestamp (for debugging / logs)

        Embedding is stored as a Python list so it can be saved in JSON.
        """
        self.cache[doc_id] = {
            "hash": doc_hash,
            "embedding": embedding.tolist(),
            "updated_at": time.time(),
        }
        self.save_cache()

