# 🔬 Self-Correcting Research Agent

A locally-running AI research agent built with LangGraph and Ollama that autonomously searches the web, synthesizes answers, and self-corrects its output through a structured critique loop — with zero API costs.

---

## 🧠 How It Works

The agent is modeled as a **finite state machine** with 4 specialized nodes:

```
User Query
    ↓
[Planner]  → Decomposes query into 3 focused sub-questions
    ↓
[Searcher] → Fetches real-time web results via DuckDuckGo
    ↓
[Analyst]  → Synthesizes a structured answer
    ↓
[Critic]   → Evaluates quality → Approves or rejects with critique
    ↓
  Approved? ─── YES ──→ Final Answer
      │
      NO
      │
      └──→ Back to [Planner] with refined query (max 3 iterations)
```

The **self-correction loop** is the core innovation: the Critic node returns structured feedback that the Planner uses to generate better search queries on the next iteration.

---

## 🛠️ Tech Stack

| Tool | Role | Why |
|------|------|-----|
| [LangGraph](https://github.com/langchain-ai/langgraph) | Agent graph framework | Only framework with native cycle/loop support and persistent checkpointed state |
| [Ollama](https://ollama.ai) | Local LLM server | Runs `qwen2.5:14b` locally with an OpenAI-compatible API — zero cost, full privacy |
| [Pydantic v2](https://docs.pydantic.dev) | State & output validation | Validates structured output at every node boundary, catching LLM formatting errors early |
| [DDGS](https://github.com/deedy5/ddgs) | Web search tool | No API key required, returns structured results suitable for LLM consumption |
| [LangChain Ollama](https://python.langchain.com) | LLM interface | Seamless integration between LangGraph nodes and local Ollama models |

---

## 📁 Project Structure

```
research-agent/
│
├── state.py              # Shared AgentState TypedDict — the agent's memory
├── config.py             # Centralized configuration (model, iterations, temperature)
├── tools.py              # DuckDuckGo search wrapper
├── nodes/
│   ├── planner.py        # Decomposes query into sub-questions
│   ├── searcher.py       # Executes web searches
│   ├── analyst.py        # Synthesizes final answer
│   └── critic.py         # Evaluates and critiques the answer
├── graph.py              # Assembles the LangGraph state machine
├── main.py               # Entry point
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- macOS / Linux
- Python 3.11+
- [Ollama](https://ollama.ai) installed and running

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/research-agent.git
cd research-agent
```

### 2. Create and activate environment
```bash
conda create -n research-agent python=3.12
conda activate research-agent
```

### 3. Install dependencies
```bash
pip install langgraph langchain-ollama ddgs pydantic
```

### 4. Pull the model
```bash
ollama pull qwen2.5:14b
```

### 5. Run the agent
```bash
python main.py
```

---

## 🔧 Configuration

Edit `config.py` to customize the agent:

```python
MODEL_NAME = "qwen2.5:14b"      # Swap for any Ollama model
OLLAMA_BASE_URL = "http://localhost:11434"
MAX_ITERATIONS = 3               # Maximum self-correction loops
TEMPERATURE = 0.0                # Lower = more deterministic output
```

---

## 💡 Example Output

**Query:** `"What are the health benefits of green tea?"`

```
Final Answer:
Green tea offers a variety of health benefits due to its rich content 
of antioxidants called catechins:

1. Heart Health: Lowers LDL cholesterol and reduces risk of heart disease
2. Blood Sugar Regulation: Helps manage diabetes
3. Cancer Prevention: Antioxidants inhibit tumor growth
4. Weight Management: Increases thermogenesis and calorie burning
5. Brain Health: Protects against neurodegenerative diseases
```

---

## 🏗️ Key Architectural Decisions

**Why TypedDict over Pydantic BaseModel for State?**
LangGraph needs to merge partial state updates between nodes. `TypedDict` with `Annotated` reducers supports this natively — `BaseModel` validates on instantiation and cannot merge partial updates.

**Why is the iteration guard in the Critic node?**
The Critic is the only node that decides whether a loop has occurred. Centralizing the guard there keeps routing logic in one place and makes the safety mechanism explicit.

**Why TEMPERATURE=0.0?**
The Critic must return consistent, parseable JSON. Higher temperature introduces randomness that breaks Pydantic validation and causes routing failures.

---

## 🚀 Future Improvements

- [ ] Add memory/checkpointing for multi-session research
- [ ] Swap DuckDuckGo for Tavily for higher quality sources
- [ ] Add a confidence score to the Analyst's output
- [ ] Build a Streamlit UI for interactive querying
- [ ] Support multiple LLM backends (OpenAI, Anthropic)

---

## 📄 License

MIT License — feel free to use and build on this project.
