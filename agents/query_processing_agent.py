import os
import openai
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def classify_legal_domain(query: str) -> str:
    """
    Uses OpenAI LLM to:
    1. **Check if the query is safe to process.**
    2. **Classify the legal domain (Civil Law, Criminal Law, Both, or NA).**

    :param query: User's input legal question.
    :return: Legal domain category OR a safety warning.
    """

    # **Step 1: Check for Unsafe or Improper Queries**
    safety_prompt = f"""
    You are a legal AI assistant. Your first task is to analyze whether this query is **safe to process** or if it requires ethical intervention.

    ### **🚨 Safety Guidelines:**
    - If the query **incites violence, promotes crime, or encourages self-harm**, respond with:  
      `"This query involves harm or unethical actions. Please seek professional legal help."`
    - If the query **is a legal question about crimes and punishments** (e.g., “What happens if I commit theft?”), respond with: `"Safe"`
    - If the query is **non-legal, vague, or lacks legal relevance**, respond with: `"Not a legal query."`
    - If the query **is about foreign laws**, respond with: `"Not Applicable in Indian Law."`

    ### **Query:**  
    "{query}"

    ### **📌 Response Format (STRICTLY FOLLOW THIS)**
    - If Safe for legal classification: Safe
    - If Harmful or Unethical: This query involves harm or unethical actions. Please seek professional legal help.
    - If Not a Legal Question: Not a legal query.
    - If Not Applicable to Indian Law: Not Applicable in Indian Law.
    """

    safety_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a legal safety filter ensuring queries are ethical and appropriate."},
                  {"role": "user", "content": safety_prompt}],
        temperature=0.1
    )

    safety_check = safety_response.choices[0].message.content.strip()

    # 🚨 **If the query is unsafe or irrelevant, return the warning immediately**
    if safety_check != "Safe":
        return safety_check

    # **Step 2: Proceed with Legal Classification ONLY if Safe**
    prompt = f"""
    You are an **Indian legal assistant**, and your task is to classify legal queries **ONLY based on Indian laws** into one of three categories:
    - **"civil_law"** (Civil Law: Disputes related to marriage, property, contracts, family, business, etc.).
    - **"criminal_law"** (Offenses punishable under IPC, fraud, crimes, etc.).
    - **"both"** (If the case involves violations of both Civil and Criminal Law).

    ---
    Then, classify it based on the following criteria:
    ### **📌 Important Instruction:**
    🚨 **Strictly follow only the legal framework of India.** 🚨  
    🚨 **If a query involves an area of law that does not exist in India, classify it as "Not Applicable in Indian Law".** 🚨  

    ---

    ### **📌 Classification Criteria (Considering ALL Indian Laws)**
    You must analyze the query based on **legal principles** rather than specific law names:

    ####Civil Law (General Law) Applies When:**
    The case involves **private disputes** between individuals or entities.  
    The issue relates to **personal rights & obligations** under Indian **family, property, business, labor, or consumer laws**.  
    The resolution involves **legal remedies such as compensation, court orders, or compliance** (not punishment).  
    Examples include:  
    - **Marriage, Divorce, Maintenance, Child Custody.**  
    - **Property Disputes, Inheritance, Land Ownership.**  
    - **Business Contracts, Financial Agreements, Consumer Rights, Employment Laws.**  

    ####Criminal Law Applies When:
    The case involves **an act punishable under Indian Penal Code (IPC) or other Indian criminal laws**.  
    The offense is legally **punishable by imprisonment, fines, or state prosecution**.  
    The case includes elements like **fraud, violence, financial crimes, abuse, public safety violations, or cyber offenses**.  
    Examples include:  
    - **Murder, Theft, Fraud, Cybercrimes, Financial Crimes.**  
    - **Sexual Harassment, Domestic Violence, Kidnapping.**  
    - **Public Safety Violations, Corruption, Criminal Breach of Trust.**  

    ####Both Civil & Criminal Laws Apply When:
    The case has **both a personal dispute (civil)** AND **an offense punishable under criminal law**.  
    Examples include:  
    - **Bigamy:** A civil marriage dispute + IPC 494 for criminal bigamy.  
    - **Domestic Violence:** Divorce & protection orders (civil) + Assault or cruelty (criminal).  
    - **Fraud in Business:** Contract disputes (civil) + Financial fraud or misrepresentation (criminal).  
    - **Sexual Harassment at Work:** Workplace rights violation (civil) + Criminal punishment for sexual offenses.  

    ---

    # ### **📌 Output Format (STRICTLY FOLLOW THIS)**
    # - **If Civil Only:** `"General Law, Civil Score: X%, Criminal Score: Y%"`  
    # - **If Criminal Only:** `"Criminal Law, Civil Score: X%, Criminal Score: Y%"`  
    # - **If Both:** `"Both, Civil Score: X%, Criminal Score: Y%"`  
    # - **If Not Applicable in Indian Law:** `"Not Applicable in Indian Law"`  

    - OUTPUT format - Just the classification mentioned in quotes, no extra text:
    -If Civil Only: civil_law
    -If Criminal Only: criminal_law  
    -If Both: both
    -If Not Applicable in Indian Law: na
    ---

    ### **Query:**  
    "{query}"  

    ### **Analyze the case carefully and return the classification only as mentioned in OUTPUT format. DO NOT rely on keywords. Focus on legal violations and consequences. Ensure that ALL civil and criminal laws applicable in India are considered dynamically. STRICTLY IGNORE ANY FOREIGN LAWS OR LEGAL PRINCIPLES.**  
    """


    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" if you prefer a cheaper option
        messages=[{"role": "system", "content": "You are a Indian legal classifier."},
                  {"role": "user", "content": prompt}],
        temperature=0.1  # Keep deterministic classification
    )

    # return response["choices"][0]["message"]["content"].strip()
    return response.choices[0].message.content


# Example Usage
if __name__ == "__main__":
    example_query = input("Enter your legal query: ")
    result = classify_legal_domain(example_query)
    print(f"{result}")  # Output: "civil_law", "criminal_law", "both", "na", or a safety warning.
