# main.py
from graph import app
from state import AgentState

if __name__ == "__main__":
    initial_state: AgentState = {
        "original_query": "What are the health benefits of green tea?",
        "search_queries": [],
        "search_results": [],
        "final_answer": "",
        "critique": "",
        "iteration_count": 0,
        "approved": False,
        "refined_query": ""
    }
    final_state = app.invoke(initial_state)
    print("Final Answer:", final_state.get("final_answer", "No answer generated."))