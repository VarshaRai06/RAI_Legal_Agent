import langgraph
from  agents.retrieval_context import retrieve_legal_text
from agents.evaluation_agent import evaluate_llm_responses

# ✅ Step 1: Initialize LangGraph
graph = langgraph.Graph()

# ✅ Step 2: Add Named Agent Nodes
# graph.add_node("query_processing", query_processing_agent)
graph.add_node("retrieval_agent", retrieve_legal_text)
# graph.add_node("llm", llm_agent)
# graph.add_node("evaluation", evaluation_agent)
# graph.add_node("fact_checking", fact_checking_agent)
# graph.add_node("responsible_ai", responsible_ai_agent)

# ✅ Step 3: Define Execution Flow Using Node Names
graph.set_entry_point("query_processing")  # Start with Query Processing
graph.add_edge("query_processing", "retrieval")  # Query Processing → Retrieval
graph.add_edge("retrieval", "llm")  # Retrieval → LLM
graph.add_edge("llm", "evaluation")  # LLM → Evaluation
graph.add_edge("evaluation", "fact_checking")  # Evaluation → Fact-Checking
graph.add_edge("fact_checking", "responsible_ai")  # Fact-Checking → Responsible AI

print("✅ LangGraph Execution Graph Defined with Named Nodes!")

# ✅ Step 4: Test LangGraph Execution
if __name__ == "__main__":
    user_query = "How can I take divorce according to Hindu law?"
    response = graph.execute(user_query)
    print("✅ Final Output:", response)