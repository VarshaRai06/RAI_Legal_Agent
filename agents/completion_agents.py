from agents.retrieval_context import retrieve_legal_text
from agents.LLM import call_llm_with_citation_test
from agents.evaluation_agent import process_evaluation
import json

def retrieval_agent(state):
    """
    Fetches relevant legal texts from ChromaDB.
    """
    print(f"🔹 Retrieval Agent Fetching Text for: {state.query} ({state.law_type})")

    # ✅ Call Retrieval Logic
    retrieved_texts = retrieve_legal_text(state.query, state.law_type)

    # ✅ Debugging Print
    print(f"DEBUG: Retrieved Texts Before Storing → {retrieved_texts}")

    # ✅ Ensure Retrieved Texts are Stored in Correct State Key
    if isinstance(retrieved_texts, list) and all(isinstance(text, dict) for text in retrieved_texts):
        state.retrieved_texts = retrieved_texts  # ✅ Correct Storage
    else:
        print("⚠️ Warning: Retrieved texts are not in a valid format! Resetting to empty.")
        state.retrieved_texts = []

    print(f"✅ Stored Retrieved Texts: {len(state.retrieved_texts)} → {state.retrieved_texts}")
    
    return state




def llm_agent(state):
    """
    Generates a response using retrieved legal text.
    """
    print(f"🔹 LLM Agent Generating Response for: {state.query}")

    # ✅ Ensure Retrieved Texts Exist Before Calling LLM
    if not state.retrieved_texts or not isinstance(state.retrieved_texts, list):
        print("⚠️ Warning: No retrieved texts available! LLM cannot generate response.")
        state.llm_responses = []  # ✅ Prevents errors in evaluation
        return state

    # ✅ Extract Only the Legal Texts
    retrieved_texts_str = " ".join([text.get("text", "") for text in state.retrieved_texts])

    # ✅ Call LLM and Ensure Proper Response Format
    llm_responses = call_llm_with_citation_test(state.query, retrieved_texts_str)

    # ✅ Debugging Print
    print(f"DEBUG: LLM Responses Before Storing → {llm_responses}")

    # ✅ Ensure LLM Response is a List of Dictionaries
    if isinstance(llm_responses, list) and all(isinstance(resp, dict) for resp in llm_responses):
        state.llm_responses = llm_responses  # ✅ Store properly structured responses
    else:
        print("⚠️ Warning: LLM response is not a valid JSON list of dictionaries! Resetting to empty.")
        state.llm_responses = []  # ✅ Prevents errors

    print(f"✅ Stored LLM Responses: {len(state.llm_responses)} → {state.llm_responses}")
    
    return state








def evaluation_agent(state):
    """
    Evaluates the LLM response using NLP metrics and selects top responses.
    """
    print(f"🔹 Evaluation Agent Scoring Response for LLM Output.")

    # ✅ Debugging Prints
    print("DEBUG: Retrieved Texts →", state.retrieved_texts)
    print("DEBUG: LLM Responses →", state.llm_responses)

    # ✅ Ensure LLM Responses are in the Correct Format
    if not isinstance(state.llm_responses, list) or not all(isinstance(resp, dict) for resp in state.llm_responses):
        print("⚠️ Error: LLM responses are not in the correct format!")
        state.top_responses = []
        state.clubbed_reference_text = ""
        return state  # ✅ Return early to prevent error

    # ✅ Check If Retrieved Texts Are Empty
    if not state.retrieved_texts:
        print("⚠️ Warning: Retrieved texts are empty! Evaluation cannot proceed.")
        state.top_responses = []
        state.clubbed_reference_text = ""
        return state  # ✅ Return early to prevent error

    # ✅ Call `process_evaluation()` and get results
    top_responses, clubbed_reference_text = process_evaluation(state.llm_responses, state.retrieved_texts)

    # ✅ Store in State
    state.top_responses = top_responses
    state.clubbed_reference_text = clubbed_reference_text

    print(f"✅ Top Responses Stored: {len(top_responses)}")
    print(f"✅ Clubbed Reference Text Stored")

    return state  # ✅ Return updated state





# def relevancy_agent(state):
#     """
#     Verifies the accuracy of LLM-generated legal responses.
#     """
#     print(f"🔹 Fact-Checking Agent Verifying Response.")

#     state.fact_checked_response = verify_legal_facts(state.llm_responses, state.evaluation_scores)  # ✅ Store fact-checked response
#     return state  # ✅ Return updated state

# def responsible_ai_agent(state):
#     """
#     Applies Responsible AI checks (bias, anonymity, privacy).
#     """
#     print(f"🔹 Responsible AI Agent Ensuring Fairness & Anonymity.")

#     state.final_response = apply_responsible_ai_checks(state.fact_checked_response)  # ✅ Store final response
#     return state  # ✅ Return updated state
