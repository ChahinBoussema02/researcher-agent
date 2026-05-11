# nodes/critic.py
from langchain_ollama import ChatOllama
from config import MODEL_NAME, OLLAMA_BASE_URL, TEMPERATURE, MAX_ITERATIONS
from state import AgentState
from pydantic import BaseModel

class CriticOutput(BaseModel):
    approved: bool
    critique: str
    refined_query: str

llm = ChatOllama(model=MODEL_NAME, temperature=TEMPERATURE, base_url=OLLAMA_BASE_URL)

def critic(state: AgentState) -> dict:
    if state["iteration_count"] >= MAX_ITERATIONS:
        return {"approved": True, "critique": "No critiques", "refined_query": state["original_query"], "iteration_count": state["iteration_count"]}

    prompt = f"""You are a research critic. Evaluate the answer below.
    Question: {state["original_query"]}
    Answer: {state["final_answer"]}
    Return ONLY a JSON object with fields: approved (bool), critique (str), refined_query (str)."""

    response = llm.invoke(prompt)
    try:
        output = CriticOutput.model_validate_json(response.content.strip())
        return {**output.model_dump(), "iteration_count": state["iteration_count"] + 1}
    except Exception as e:
        return {"approved": False, "critique": f"Parse error: {e}", "refined_query": state["original_query"], "iteration_count": state["iteration_count"] + 1}