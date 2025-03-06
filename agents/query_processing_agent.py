import os
import openai
from dotenv import load_dotenv

# Load API Key from .env file and set it
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY


def classify_legal_domain(query: str) -> str:
    """
    Uses OpenAI LLM to classify the legal domain (General Law or Criminal Law).

    :param query: User's input legal question.
    :return: Legal domain category as a string.
    """

    prompt = f"""
    You are an INDIAN legal assistant specializing in classifying legal queries into one of three categories:
    - **"General Law" (Family Law, Civil Law, Property, Divorce, Wills, etc.)**
    - **"Criminal Law" (Murder, Theft, Cybercrime, Fraud, Punishment, Charges, etc.)**
    - **"Both" (If the query involves aspects of both General and Criminal Law)**

    ### **Instructions:**
    1. **Analyze the legal query carefully** and determine whether it belongs to:
    - **General Law** (Civil cases related to marriage, property, contracts, family disputes, etc.).
    - **Criminal Law** (Cases involving punishment, crimes, fraud, offenses, etc.).
    - **Both** (If the query has aspects of both legal domains).
    
    2. **Assign Confidence Scores:**
    - Assign a **Civil Law Score** (percentage between 0% - 100%).
    - Assign a **Criminal Law Score** (percentage between 0% - 100%).
    - Ensure that **Civil Score + Criminal Score = 100%**.

    3. **Output Format (STRICTLY FOLLOW THIS FORMAT):**
    - **General Law Only:** `"General Law, Civil Score: 90%, Criminal Score: 10%"`
    - **Criminal Law Only:** `"Criminal Law, Civil Score: 10%, Criminal Score: 90%"`
    - **Both:** `"Both, Civil Score: 50%, Criminal Score: 50%"`

    ### **Query:**  
    "{query}"

    ### **Return ONLY the classification and scores in the exact format. No extra explanation.**  
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" if you prefer a cheaper option
        messages=[{"role": "system", "content": "You are a Indian legal classifier."},
                  {"role": "user", "content": prompt}],
        temperature=0.1  # Keep deterministic classification
    )

    # return response["choices"][0]["message"]["content"].strip()
    return response.choices[0].message.content

# from utils import call_llm

# def classify_legal_domain(query: str) -> str:
#     """
#     Uses OpenAI LLM to classify the legal domain (General Law or Criminal Law).

#     :param query: User's input legal question.
#     :return: Legal domain category as a string.
#     """

#     prompt = f"""
#     You are a legal assistant. Classify the following legal query into one of two categories:
#     - "General Law" (Family Law, Civil Law, Property, Divorce, Wills, etc.)
#     - "Criminal Law" (Murder, Theft, Cybercrime, Fraud, Punishment, Charges, etc.)
    
#     Respond ONLY with either "General Law" or "Criminal Law".
    
#     Query: "{query}"
#     """

#     return call_llm(prompt, model="gpt-4", temperature=0.1)



# Example Usage
if __name__ == "__main__":
    example_query = input()
    result = classify_legal_domain(example_query)
    print(f"Legal Domain: {result}")  # Expected Output: "General Law" or "Criminal Law"
