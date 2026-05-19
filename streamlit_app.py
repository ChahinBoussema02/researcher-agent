import streamlit as st
from graph import app

st.title("🔬 Self-Correcting Research Agent")

query = st.text_input("Enter your research query:")

if st.button("Run Agent"):
    with st.spinner("Researching..."):
        final_state = app.invoke({
            "original_query": query,
            "search_queries": [],
            "search_results": [],
            "final_answer": "",
            "critique": "",
            "iteration_count": 0,
            "approved": False,
            "refined_query": "",
            "confidence": 0.0
        })
    st.success(final_state.get("final_answer", "No answer generated."))
    st.metric(label="Confidence", value=f"{final_state.get('confidence', 0.0) * 100:.1f}%")
    st.info(f"Iterations taken: {final_state.get('iteration_count', 0)}")