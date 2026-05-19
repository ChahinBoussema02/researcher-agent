# graph.py
from langgraph.graph import StateGraph, END
from state import AgentState
from nodes.planner import planner
from nodes.searcher import searcher
from nodes.analyst import analyst
from nodes.critic import critic

def route_critic(state: AgentState) -> str:
    if state.get("approved", False):
        return "end"
    return "planner"

graph = StateGraph(AgentState)

graph.add_node("planner", planner)
graph.add_node("searcher", searcher)
graph.add_node("analyst", analyst)
graph.add_node("critic", critic)

graph.add_edge("planner", "searcher")
graph.add_edge("searcher", "analyst")
graph.add_edge("analyst", "critic")
graph.add_conditional_edges(
    "critic",
    route_critic,
    {"planner": "planner", "end": END}
)

graph.set_entry_point("planner")

app = graph.compile()