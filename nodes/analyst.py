# nodes/analyst.py
import logging
from langchain_ollama import ChatOllama
from config import MODEL_NAME, OLLAMA_BASE_URL, TEMPERATURE
from state import AgentState

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

llm = ChatOllama(model=MODEL_NAME, temperature=TEMPERATURE, base_url=OLLAMA_BASE_URL)

def analyst(state: AgentState) -> dict:
    logger.info(f"Analyst started | results: {state['search_results']}")
    original_query = state["original_query"]
    results_text = "\n".join(state["search_results"])
    prompt = f"""You are a research analyst. Synthesize a concise answer to the question below.
    Ignore ads and irrelevant content.
    Question: {original_query}
    Search Results: {results_text}"""
    response = llm.invoke(prompt)
    logger.info(f"Analyst produced answer: {response.content.strip()[:100]}...")
    return {"final_answer": response.content.strip()}