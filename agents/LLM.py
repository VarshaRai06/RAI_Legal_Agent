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

    Provide all 4 responses strictly as a single JSON array (list) of dictionaries in the following format:
    [
        {{"response_id": "unique response id", "response": "legal response", "citations": "relevant citation"}}
    ]

    Do not include any additional text outside the JSON array.
    """

    # ✅ Call OpenAI GPT-4 API
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an Indian legal expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    # ✅ Extract Response Properly
    try:
        response_text = response.choices[0].message.content.strip()
        llm_responses = json.loads(response_text)  # ✅ Ensure parsing is correct
    except (json.JSONDecodeError, IndexError) as e:
        print(f"⚠️ JSON Parsing Error in LLM Response: {e}")
        return []

    # ✅ Ensure Correct Key Format (response_id, response, citations)
    formatted_responses = []
    for i, resp in enumerate(llm_responses):
        formatted_responses.append({
            "response_id": resp.get("response_id", f"resp_00{i+1}"),
            "response": resp.get("response", "No response available"),
            "citations": resp.get("citations", "No citations available")
        })

    print("\n✅ LLM Responses Generated:", formatted_responses)
    return formatted_responses  # ✅ Return properly formatted responses