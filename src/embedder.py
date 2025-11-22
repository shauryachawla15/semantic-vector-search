import os
import re
import hashlib

def clean_text(text: str) -> str:
    """
    Cleans raw text so it is easier for the model to work with.

    Steps:
    - Convert everything to lowercase
    - Remove any HTML tags (e.g., <p>, <br>)
    - Remove extra spaces and newlines

    This makes all documents consistent before generating embeddings.
    """
    text = text.lower()
    text = re.sub(r"<.*?>", " ", text)         # Remove HTML tags
    text = re.sub(r"\s+", " ", text).strip()   # Remove extra whitespace
    return text


def compute_hash(text: str) -> str:
    """
    Generates a SHA-256 hash of the cleaned text.

    We use this hash to detect if a document has changed.
    If the text is the same, we can reuse the cached embedding.
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def load_document(path: str) -> dict:
    """
    Loads a document from disk and prepares it for embedding.

    What this function does:
    1. Read the raw .txt file
    2. Clean the text using clean_text()
    3. Compute a SHA-256 hash of the cleaned text
    4. Return useful metadata

    Returns a dictionary:
    {
        'text': cleaned_text,
        'hash': sha256_hash,
        'length': number_of_characters
    }
    """
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()

    cleaned = clean_text(raw)
    doc_hash = compute_hash(cleaned)

    return {
        "text": cleaned,
        "hash": doc_hash,
        "length": len(cleaned),
    }
