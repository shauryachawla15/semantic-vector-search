from fastapi import FastAPI
from pydantic import BaseModel
from search_engine import SearchEngine

# Create the FastAPI application
app = FastAPI()

# Initialize our search engine once when the API starts
engine = SearchEngine()

# Define what a search request should look like
class SearchQuery(BaseModel):
    query: str            # The text the user wants to search for
    top_k: int = 5        # How many top results to return (default = 5)

@app.post("/search")
def search(q: SearchQuery):
    """
    This endpoint receives a search query,
    sends it to our SearchEngine,
    and returns the top matching documents.

    Example input:
    {
        "query": "computer graphics",
        "top_k": 5
    }
    """
    results = engine.search(q.query, q.top_k)
    return {"results": results}
