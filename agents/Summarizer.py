import openai  # type: ignore
import os  # For accessing environment variables

# Set up OpenAI API Key from environment variables (Keep it only once)
openai.api_key = os.getenv("OPENAI_API_KEY", "your_openai_api_key")  # Ensure this is set in VS Code

def call_summarizer_agent(query, response_1, response_2):
    """Summarize the given two responses from the relevancy agent based on the user's query."""
    
    # Construct prompt for summarization
    prompt = f"""
    You are an AI Legal Summarizer specializing in condensing legal responses while preserving key legal references and citations.
    You will summarize the responses while ensuring relevance to the user's query.
    
    ### Guidelines for Summarization:
    1. **Preserve Legal Accuracy** - Do not alter the legal meaning of statements.
    2. **Conciseness** - Retain only the most essential legal points and remove redundant details.
    3. **Maintain Citations** - Ensure that relevant legal statutes and case laws are included in the summary.
    4. **Ensure Query Relevance** - The summary should specifically address the user's legal query.
    5. **Clear & Structured Output** - Present the summary in a readable, structured format.
    6. **Objective Tone** - Keep the summary neutral and legally precise.
    
    **User Query:**
    {query}
    
    **Legal Response 1:**
    {response_1}
    
    **Legal Response 2:**
    {response_2}
    
    Summarize the above two responses while ensuring relevance to the user's query and maintaining key legal references and citations. Ensure that the most important points are retained. If there is a new line, add it below.
    """
    
    # Call OpenAI GPT-4 API for summarization (Updated for OpenAI v1.0.0+)
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.1,
        max_tokens=512,  # Reduced token limit for summarization
        n=1  # Generate 1 summarized response
    )
    
    # Extract and return the summarized response
    summary_text = response.choices[0].message.content.strip()
    return summary_text  # Return only the structured summary
