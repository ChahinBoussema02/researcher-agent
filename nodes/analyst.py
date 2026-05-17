# nodes/analyst.py
import logging
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from config import MODEL_NAME, OLLAMA_BASE_URL, TEMPERATURE
from state import AgentState

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

class AnalystOutput(BaseModel):
    answer: str
    confidence: float  # 0.0 to 1.0

llm = ChatOllama(model=MODEL_NAME, temperature=TEMPERATURE, base_url=OLLAMA_BASE_URL)

def analyst(state: AgentState) -> dict:
    logger.info(f"Analyst started | results: {state['search_results']}")
    original_query = state["original_query"]
    results_text = "\n".join(state["search_results"])
    prompt = f"""You are a research analyst. Synthesize a concise answer to the question below.
    Ignore ads and irrelevant content.
    Question: {original_query}
    Search Results: {results_text}
    Return ONLY a JSON object with fields: answer (str), confidence (float between 0.0 and 1.0)"""
    response = llm.invoke(prompt)
    try:
        output = AnalystOutput.model_validate_json(response.content.strip())
        logger.info(f"Analyst confidence: {output.confidence} | answer: {output.answer[:100]}...")
        return {"final_answer": output.answer, "confidence": output.confidence}
    except Exception as e:
        logger.error(f"Analyst parse failed: {e}")
        return {"final_answer": response.content.strip(), "confidence": 0.0}