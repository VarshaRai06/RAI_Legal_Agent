from langgraph.langgraph_executor import runnable_graph
from langgraph.langgraph_executor import AgentState  # ✅ Import AgentState to properly manage execution

def run_pipeline(user_query):
    """
    Runs the full LangGraph pipeline for the given query.
    """
    print(f"\n🚀 Running LangGraph Pipeline for Query: {user_query}")

    try:
        # ✅ Ensure Initial State is Correctly Initialized
        initial_state = AgentState(query=user_query)

        # ✅ Execute LangGraph and Retrieve Final State
        final_state_dict = runnable_graph.invoke(initial_state)  # ✅ Ensure execution returns a dictionary

        # ✅ Convert `final_state_dict` to `AgentState`
        final_state = AgentState(**final_state_dict) if isinstance(final_state_dict, dict) else final_state_dict

        # ✅ Ensure `final_response` Exists Before Printing
        if hasattr(final_state, "final_response"):
            print("\n✅ Final Processed Response:")
            print(final_state.final_response)  # ✅ Retrieve final response safely
            return final_state.final_response
        else:
            print("⚠️ Error: `final_response` not found in final state!")
            return "Error: Missing Final Response"

    except Exception as e:
        print(f"\n❌ Error during execution: {str(e)}")
        return None


if __name__ == "__main__":
    user_query = "murder charges"
    run_pipeline(user_query)
