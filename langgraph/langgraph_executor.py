from langgraph.graph import StateGraph
from pydantic import BaseModel
from typing import List
from agents.completion_agents import retrieval_agent
from agents.completion_agents import llm_agent
from agents.completion_agents import evaluation_agent

# ✅ Define Agent State
class AgentState(BaseModel):
    query: str
    law_type: str
    retrieved_texts: List[dict] = []  # ✅ Stores retrieved legal text chunks
    llm_responses: List[dict] = []  # ✅ Stores LLM-generated responses
    evaluation_scores: List[dict] = []  # ✅ Stores scores from evaluation agent
    top_responses: List[dict] = []  # ✅ Stores top-ranked responses for fact-checking
    clubbed_reference_text: str = ""  # ✅ Stores aggregated reference text
    final_response: str = ""  # ✅ Stores final fact-checked response

# ✅ Initialize StateGraph
graph = StateGraph(AgentState)

# ✅ Add Nodes (Agents)
graph.add_node("retrieval_agent", retrieval_agent)
graph.add_node("llm_agent", llm_agent)
graph.add_node("evaluation_agent", evaluation_agent)

# ✅ Define Graph Execution Flow
graph.add_edge("retrieval_agent", "llm_agent")
graph.add_edge("llm_agent", "evaluation_agent")

# ✅ Define Entry Point (Starting Node)
graph.set_entry_point("retrieval_agent")

# ✅ Compile Graph
runnable_graph = graph.compile()
print("✅ LangGraph Execution Graph Defined and Compiled!")