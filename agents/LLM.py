import openai # type: ignore
import uuid

# Set up OpenAI API Key
openai.api_key = "your_openai_api_key"  # 🔹 Replace this with your actual OpenAI API key

def call_llm_with_citation_test():
    """Test LLM response with a sample legal question and citations."""

    sample_query = "Can a person claim self-defense after injuring someone in a fight?"
    sample_context = "The person was attacked first and reacted to protect themselves."
    sample_retrieved_docs = "Relevant Laws: Indian Penal Code, 1860 - Section 96 (Right to Private Defense); Supreme Court Judgment - XYZ vs. LMN, 2019."

    # Construct prompt
    prompt = f"""
    You are an AI Legal Assistant specializing in Civil Law, trained to provide precise, legally accurate, and well-structured responses based on the retrieved legal documents.

    Your expertise covers a wide range of civil law matters, including but not limited to:
    - Contract law (agreements, breaches, enforcement)
    - Property disputes (ownership, tenancy, land regulations)
    - Family law (divorce, child custody, inheritance)
    - Business regulations (compliance, liabilities, legal obligations)

    ### Guidelines for Your Response:
    1. **Legal Accuracy** - Ensure that all responses are legally sound and supported by relevant statutes, precedents, or case laws.
    2. **Clarity & Structure** - Present information in a well-organized, easy-to-understand format.
    3. **Citations & References** - Provide citations for all legal statements, referencing relevant legal provisions, statutes, or case laws where applicable.
    4. **Objective & Neutral Tone** - Maintain a professional and neutral stance without offering personal opinions.
    5. **User-Friendly Explanations** - If legal concepts are complex, provide concise explanations in plain language for better understanding.
    6. **Citation Format** - Include citations at the end of the response in the format: (Law Name, Section, Case Law Reference, Year). Example: "According to the Contract Act, 1872, Section 10..." or "As per [Case Name], Supreme Court, 2021..."

    **Context:** {sample_context}
    **Retrieved Legal Documents:** {sample_retrieved_docs}
    **User Query:** {sample_query}

    Provide 4 distinct legally accurate responses including case laws, statutes, or references. No numbering please. No spacing between lines.
    DO NOT include 'response_id' or any formatting in the response. Just return the pure legal response as a paragraph.
    """

    # Call OpenAI GPT-4 API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.1,
        max_tokens=1024,
        n=4  # Generate 4 separate responses
    )

    # Extract and Structure Responses in the Required Format
    llm_responses = []
    for i, choice in enumerate(response["choices"]):
        response_text = choice["message"]["content"].strip()
        
        # Store responses as paragraphs in the required format
        llm_responses.append(f"Response ID: resp_00{i+1}\nResponse: {response_text} (Citation: {sample_retrieved_docs})\n")
    
    # Print responses in the required format
    print("\n\n".join(llm_responses))

    return llm_responses  # Return the structured responses only

# Run the Test
if __name__ == "__main__":
    output = call_llm_with_citation_test()