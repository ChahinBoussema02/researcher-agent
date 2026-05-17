# nodes/critic.py
import logging

from langchain_ollama import ChatOllama
from config import MODEL_NAME, OLLAMA_BASE_URL, TEMPERATURE, MAX_ITERATIONS
from state import AgentState
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

class CriticOutput(BaseModel):
    approved: bool
    critique: str
    refined_query: str

llm = ChatOllama(model=MODEL_NAME, temperature=TEMPERATURE, base_url=OLLAMA_BASE_URL)

def critic(state: AgentState) -> dict:
    logger.info(f"Critic started | iteration: {state['iteration_count']}")
    if state["iteration_count"] >= MAX_ITERATIONS:
        return {"approved": True, "critique": "No critiques", "refined_query": state["original_query"], "iteration_count": state["iteration_count"]}

    prompt = f"""You are a research critic. Evaluate the answer below.
    Question: {state["original_query"]}
    Answer: {state["final_answer"]}
    Return ONLY a JSON object with fields: approved (bool), critique (str), refined_query (str)."""

    response = llm.invoke(prompt)
    logger.info(f"Critic raw response: {response.content.strip()[:100]}...")
    try:
        output = CriticOutput.model_validate_json(response.content.strip())
        logger.info(f"Critic decision | approved: {output.approved}")
        return {**output.model_dump(), "iteration_count": state["iteration_count"] + 1}
    except Exception as e:
        logger.error(f"Critic parse failed: {e}")
        return {"approved": False, "critique": f"Parse error: {e}", "refined_query": state["original_query"], "iteration_count": state["iteration_count"] + 1}