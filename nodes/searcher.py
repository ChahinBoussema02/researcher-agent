# nodes/searcher.py
import logging
from state import AgentState
from tools import search_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

def searcher(state: AgentState) -> dict:
    logger.info(f"Searcher started | queries: {state['search_queries']}")
    search_queries = state["search_queries"]
    search_results = []
    for query in search_queries:
        results = search_engine(query)
        search_results.extend(results)
    logger.info(f"Searcher produced {len(search_results)} results")
    return {"search_results": search_results}