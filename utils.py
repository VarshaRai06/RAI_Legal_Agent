import openai
from config import OPENAI_API_KEY

# Set API Key
openai.api_key = OPENAI_API_KEY

def call_llm(prompt: str, model="gpt-4", temperature=0.1, max_tokens=1024, n=1):
    """
    Calls OpenAI's GPT model with a given prompt and returns the response.

    :param prompt: The input text to be processed by LLM.
    :param model: The OpenAI model to use (default: "gpt-4").
    :param temperature: Controls randomness (default: 0.1 for deterministic output).
    :param max_tokens: Maximum response length (default: 1024).
    :param n: Number of responses to generate (default: 1).
    :return: LLM-generated response(s) as a string or a list.
    """

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            n=n
        )

        # If multiple responses are requested, return them as a list
        if n > 1:
            return [choice["message"]["content"].strip() for choice in response["choices"]]
        
        # Return a single response
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Error calling OpenAI API: {e}")
        return None
