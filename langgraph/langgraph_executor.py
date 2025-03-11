from langgraph.graph import StateGraph
from pydantic import BaseModel
from typing import List, Dict, Any
from agents.completion_agents import retrieval_agent
from agents.completion_agents import llm_agent
from agents.completion_agents import evaluation_agent
from agents.completion_agents import query_processing_agent
from agents.completion_agents import relevancy_agent
from agents.completion_agents import summarization_agent
from agents.completion_agents import responsible_ai_agent
# from agents.completion_agents i

# ✅ Define Agent State
class AgentState(BaseModel):
    query: str
    summarized_response : str = ""
    law_type: str = "unknown"  # ✅ Default value to avoid validation errors
    retrieved_texts: List[dict] = []  # ✅ Stores retrieved legal text chunks
    llm_responses: List[dict] = []  # ✅ Stores LLM-generated responses
    evaluation_scores: List[dict] = []  # ✅ Stores scores from evaluation agent
    top_responses: List[dict] = []  # ✅ Stores top-ranked responses for fact-checking
    clubbed_reference_text: str = ""  # ✅ Stores aggregated reference text
    final_response: str = ""  # ✅ Stores final fact-checked response
    # fact_checked_response: Dict[str, Any] = {}

# ✅ Initialize StateGraph
graph = StateGraph(AgentState)

# ✅ Add Nodes (Agents)
graph.add_node("query_processing_agent", query_processing_agent)
graph.add_node("retrieval_agent", retrieval_agent)
graph.add_node("llm_agent", llm_agent)
graph.add_node("evaluation_agent", evaluation_agent)
graph.add_node("relevancy_agent", relevancy_agent)
graph.add_node("summarization_agent", summarization_agent)
graph.add_node("responsible_ai_agent", responsible_ai_agent)
# ✅ Define Entry Point (Starting Node)


graph.set_entry_point("query_processing_agent")
# ✅ Define Graph Execution Flow
graph.add_edge("query_processing_agent", "retrieval_agent")
graph.add_edge("retrieval_agent", "llm_agent")
graph.add_edge("llm_agent", "evaluation_agent")
graph.add_edge("evaluation_agent", "relevancy_agent")
graph.add_edge("relevancy_agent", "summarization_agent")
graph.add_edge("summarization_agent", "responsible_ai_agent")

graph.set_finish_point("responsible_ai_agent")


# ✅ Compile Graph
runnable_graph = graph.compile()
print("✅ LangGraph Execution Graph Defined and Compiled!")