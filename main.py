from langgraph.langgraph_executor import runnable_graph

def run_pipeline(user_query, law_type):
    """
    Runs the full LangGraph pipeline for the given query.
    """
    print(f"\n🚀 Running LangGraph Pipeline for Query: {user_query}")

    try:
        state = runnable_graph.invoke({"query": user_query, "law_type":law_type})  # ✅ Use state-based execution

        print("\n✅ Final Processed Response:")
        print(state.final_response)  # ✅ Retrieve final response from memory
        return state.final_response

    except Exception as e:
        print(f"\n❌ Error during execution: {str(e)}")
        return None


if __name__ == "__main__":
    user_query = "Punishment for murder"
    law_type = "criminal_law"
    run_pipeline(user_query,law_type)