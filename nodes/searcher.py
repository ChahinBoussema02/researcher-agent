# nodes/searcher.py
from state import AgentState
from tools import search_engine

def searcher(state: AgentState) -> dict:
    search_queries = state["search_queries"]
    search_results = []
    for query in search_queries:
        results = search_engine(query)
        search_results.extend(results)
    return {"search_results": search_results}