# nodes/planner.py
from langchain_ollama import ChatOllama
from config import MODEL_NAME, OLLAMA_BASE_URL, TEMPERATURE
from state import AgentState
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

llm = ChatOllama(model=MODEL_NAME, temperature=TEMPERATURE, base_url=OLLAMA_BASE_URL)

def planner(state: AgentState) -> dict:
    query = state['original_query'] if state["iteration_count"] == 0 else state['refined_query']
    logger.info(f"Planner started | iteration: {state['iteration_count']} | query: {query}")
    prompt = f"""Decompose this research question into exactly 3 focused search queries.
    Return only a numbered list, nothing else.
    Question: {query}"""
    response = llm.invoke(prompt)
    queries = [line.strip() for line in response.content.strip().split("\n") if line.strip()]
    logger.info(f"Planner produced queries: {queries}")
    return {"search_queries": queries}
