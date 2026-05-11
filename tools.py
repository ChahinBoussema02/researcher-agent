# tools.py
from ddgs import DDGS
from config import MAX_ITERATIONS

def search_engine(query: str, max_results: int = 5) -> list[str]:
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(f"URL: {r['href']} | Content: {r['body']}")
    return results
