from typing import Annotated
from langgraph.graph import add_messages
from typing_extensions import TypedDict

class AgentState(TypedDict):
    original_query: str
    search_queries: list[str]
    search_results: list[str]
    final_answer: str
    critique: str
    refined_query: str
    iteration_count: int
    approved: bool
    confidence: float