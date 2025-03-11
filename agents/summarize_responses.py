import openai  # type: ignore
import os  # For accessing environment variables
import json
from config import OPENAI_API_KEY
# Set up OpenAI API Key from environment variables
openai.api_key = OPENAI_API_KEY


def call_summarizer_agent(query, top_responses, retrieved_context):
    """Summarize the top responses from the evaluation agent based on the user's query and retrieved context."""

    response_1_text = top_responses[0]["response"] if len(top_responses) > 0 else "Not Found"
        
    response_1_citation = top_responses[0]["citations"] if len(top_responses) > 0 else "Not Found"

    response_2_text = top_responses[1]["response"] if len(top_responses) > 1 else "Not Found"
    response_2_citation = top_responses[1]["citations"] if len(top_responses) > 0 else "Not Found"

    # Construct prompt for summarization
    prompt = f"""
    You are an AI Legal Summarizer specializing in condensing legal responses while preserving key legal references and citations.

    Guidelines for Summarization:
    1. Preserve Legal Accuracy - Do not alter the legal meaning.
    2. Conciseness - Retain only essential legal points.
    3. Maintain Citations - Include relevant citations.
    4. Context Awareness - Incorporate information from the retrieved context.
    5. Query Relevance - Directly address the user's legal query.
    6. Clear & Structured Output - Provide a clear and structured summary.
    7. Objective Tone - Neutral and precise.

    User Query:
    {query}

    Retrieved Context:
    {retrieved_context}

    Legal Response 1:
    {response_1_text} (Citation: {response_1_citation})

    Legal Response 2:
    {response_2_text} (Citation: {response_2_citation})

    Provide the summarized response strictly in JSON dictionary format:
    {{
        "query": "{query}",
        "summary": "Summarized legal response considering retrieved context",
        "citations": ["{response_1_citation}", "{response_2_citation}"]
    }}

    Do not include additional text outside this JSON.
    """

    # Call OpenAI GPT-4 API for summarization
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.1,
        max_tokens=512,
        n=1
    )

    # Extract and return the summarized response
    response_content = response.choices[0].message.content.strip()
    summarized_response = json.loads(response_content)

    return summarized_response