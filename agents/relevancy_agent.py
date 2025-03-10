import openai
import os
import re
from dotenv import load_dotenv
from transformers import AutoModel, AutoTokenizer
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load API Key from .env file and set it
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY

# Explicitly specify OpenAI API type
openai.api_type = "openai"  # Fix for ambiguous module client error

# Load bge-m3 model and tokenizer
model_name = "BAAI/bge-m3"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def detect_hallucination(cosine_similarity_score, groundness_score):
    """
    Combines cosine similarity (query-response) with groundness (context-response)
    to detect hallucination.
    """
    if cosine_similarity_score > 0.7 and groundness_score > 0.7:
        return("✅ No Hallucination")
    elif cosine_similarity_score > 0.7 and groundness_score <= 0.7:
        return("⚠️ Partial Hallucination (Relevant but lacks factual grounding)")
    else:
        return("❌ Hallucinated Response")


def get_bge_m3_embedding(text):
    """Encodes a given text into an embedding using bge-m3."""
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
    
    with torch.no_grad():
        model_output = model(**inputs)
    
    # Use mean pooling (recommended for BGE models)
    embedding = model_output.last_hidden_state.mean(dim=1)  # Shape: (1, hidden_dim)
    return embedding.squeeze().numpy()  # Convert to NumPy array


def cosine_similarity_func(question, response):
    """Computes cosine similarity between question and response embeddings using bge-m3."""
    query_embedding = get_bge_m3_embedding(question)
    response_embedding = get_bge_m3_embedding(response)
    
    # Reshape for sklearn's cosine_similarity function
    query_embedding = query_embedding.reshape(1, -1)
    response_embedding = response_embedding.reshape(1, -1)
    
    cosine_sim = cosine_similarity(query_embedding, response_embedding)
    return cosine_sim[0][0]


def generate_llm_score(system_prompt, user_input):
    """
    Generic function to query an LLM (GPT-3.5 or any other model)
    and return a float score between 0.0 and 1.0.
    """
    try:

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}],
            temperature=0.1, # Keep deterministic classification
            max_tokens=10
        )

        # Extract the response text
        raw_output = response.choices[0].message.content.strip()

        # Ensure the output is strictly a float between 0.0 and 1.0
        match = re.search(r"(\d+\.\d{1,2})", raw_output)
        if match:
            return float(match.group(1))  # Convert extracted number to float
        else:
            return 0.0  # Default to 0 if parsing fails (preventing errors)

    except Exception as e:
        print(f"Error in LLM call: {e}")
        return 0.0  # Return 0 on failure


def answer_relevance(response, question):
    """Evaluates how relevant the response is to the given query."""
    system_prompt = """A user will give you a response and a question. 
    Your task is to rate how relevant the response is to the question. 
    Answer must be a number between 0.0 and 1.0 rounded to two decimal places. 
    0.0 means completely irrelevant, 1.0 means perfectly relevant."""
    
    user_input = f"Response: {response} Question: {question}"
    return generate_llm_score(system_prompt, user_input)


def context_relevance(context, question):
    """Evaluates how well the retrieved context matches the query."""
    system_prompt = """A user will give you a context and a question.
    Your task is to rate how relevant the context is to the question.
    Answer must be a number between 0.0 and 1.0 rounded to two decimal places.
    0.0 means completely irrelevant, 1.0 means perfectly relevant."""
    
    user_input = f"Context: {context} Question: {question}"
    return generate_llm_score(system_prompt, user_input)


def groundness(context, response):
    """Evaluates how well the response is grounded in the retrieved context."""
    system_prompt = """A user will give you a response and a context.
    Your task is to rate how much the response is supported by the context.
    Answer must be a number between 0.0 and 1.0 rounded to two decimal places.
    0.0 means response is not at all supported, 1.0 means fully supported."""
    
    user_input = f"Context: {context} Response: {response}"
    return generate_llm_score(system_prompt, user_input)


def evaluate_relevance(query, response1, response2, retrieved_context):
    """
    Evaluates both responses using the RAG Triad (Answer Relevance, Context Relevance, Groundedness).
    """
    results = {}

    for i, response in enumerate([response1, response2], start=1):
        print(f"\nEvaluating Response {i}...")

        answer_rel = answer_relevance(response, query)
        context_rel = context_relevance(retrieved_context, query)
        ground = groundness(retrieved_context, response)
        cosine_similarity_score = cosine_similarity_func(query, response)
        hallucination = detect_hallucination(cosine_similarity_score, ground)

        results[f"Response_{i}"] = {
            "Answer Relevance": answer_rel,
            "Context Relevance": context_rel,
            "Groundedness": ground,
            "Cosine Similarity": cosine_similarity_score,
            "Hallucination Result": hallucination
        }

        print(f"Response {i} Scores:\n"
              f"  Answer Relevance: {answer_rel}\n"
              f"  Context Relevance: {context_rel}\n"
              f"  Groundedness: {ground}\n"
              f"  Cosine Similarity: {cosine_similarity_score}\n"
              f"  Hallucination Result: {hallucination}\n")

    return results


def fact_checking_agent(query, top_responses, retrieved_context):
    """
    Verifies the accuracy of LLM-generated legal responses.
    """
    response1 = top_responses.get("response_1", {}).get("text", "Not Found")
    response2 = top_responses.get("response_2", {}).get("text", "Not Found")

    print(f"🔹 Fact-Checking Agent Verifying Response.")

    # Run evaluation
    relevance_scores = evaluate_relevance(query, response1, response2, retrieved_context)

    # Print final results
    print("\nFinal Relevance Scores:", relevance_scores)

    # Uncomment the below line to return the query (string) and the top_responses (dictionary) to the next agent
    # return query, top_responses


'''
# === EXAMPLE USAGE ===
if __name__ == "__main__":
    
    query = "What is the penalty for breach of contract?"
    top_responses = {
        "response_1": {
            "text": "The penalty for breach of contract is usually a fine or damages awarded by the court.",
            "citation": "civil pdf"
        }, 
        "response_2": {
            "text": "In India, breach of contract leads to imprisonment for up to 5 years, as per the Civil Code.",
            "citation": "criminal pdf"
        }
    }
    retrieved_context = "Breach of contract typically results in monetary damages. In some cases, specific performance may be ordered."
    
    fact_checking_agent(query, top_responses, retrieved_context)'
'''