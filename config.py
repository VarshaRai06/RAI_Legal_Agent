import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Direct variable assignment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Example usage
if __name__ == "__main__":
    print(f"Loaded OpenAI API Key: {'✔️ Loaded' if OPENAI_API_KEY else '❌ Not Found'}")
