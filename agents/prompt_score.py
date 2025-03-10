import openai  # OpenAI Moderation API for safety checks
import os
import re
import matplotlib.pyplot as plt
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from Dbias.bias_classification import classifier
from dotenv import load_dotenv
import nltk
nltk.download('vader_lexicon')


# Load API Key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY
openai.api_type = "openai"  # Explicitly set API type

### 🔹 Step 1: Prompt Safety using OpenAI Moderation API
def moderation_func(text):
    """
    Uses OpenAI Moderation API to check if the input text is safe.
    Returns moderation results.
    """
    try:
        response = openai.moderations.create(input=[text])
        return response.results[0]  # Return full moderation object
    except Exception as e:
        print(f"Error in OpenAI Moderation API: {e}")
        return {"error": str(e)}

### 🔹 Step 2: Neutrality, Subjectivity, and Polarity Scores
def calculate_scores(text):
    """
    Calculates Neutrality (VADER), Subjectivity (TextBlob), and Polarity (TextBlob).
    """
    blob = TextBlob(text)
    sia = SentimentIntensityAnalyzer()

    polarity = blob.sentiment.polarity  # [-1 to 1] Negative to Positive
    subjectivity = blob.sentiment.subjectivity  # [0 to 1] Objective to Subjective

    # VADER Sentiment Analysis (Neutrality Score)
    sentiment_scores = sia.polarity_scores(text)
    neutrality = sentiment_scores['neu']

    return {
        'neutrality': round(neutrality, 2),
        'subjectivity': round(subjectivity, 2),
        'polarity': round(polarity, 2)
    }

### 🔹 Step 3: Bias Score using Dbias
def bias_score_func(text):
    """
    Uses Dbias bias classifier and extracts the score.
    Returns the bias score as a float.
    """
    try:
        bias_result = classifier(text)
        if isinstance(bias_result, list) and len(bias_result) > 0:
            return float(bias_result[0]['score'])  # Extract numeric bias score
        return 0.0
    except Exception as e:
        print(f"Error in Dbias Bias Classifier: {e}")
        return 0.0  # Return 0 if error

### 🔹 Step 4: Extract Moderation Scores
def extract_moderation_scores(moderation_result):
    """
    Extracts and filters moderation scores where values > 0.5.
    Returns a sorted dictionary of significant categories.
    """
    if "error" in moderation_result:
        return {}

    # Extract category scores from OpenAI moderation response
    scores = {
        k: round(v, 2) if v is not None else 0.0  # Convert None values to 0.0
        for k, v in moderation_result.category_scores.__dict__.items()
    }
    
    # Keep only high-scoring categories (> 0.5)
    filtered_scores = {k: v for k, v in scores.items() if v > 0.5}
    return dict(sorted(filtered_scores.items(), key=lambda item: item[1], reverse=True))

### 🔹 Step 5: Unified Prompt Analysis Function
def analyze_prompt(text):
    """
    Runs all safety and bias checks on a given text.
    Returns a dictionary with results.
    """
    print(f"\n🔍 Analyzing Prompt: {text}\n")

    moderation_result = moderation_func(text)
    nsp_scores = calculate_scores(text)
    bias = bias_score_func(text)
    moderation_scores = extract_moderation_scores(moderation_result)

    analysis_result = {
        "Moderation Scores": moderation_scores,
        "Neutrality": nsp_scores["neutrality"],
        "Subjectivity": nsp_scores["subjectivity"],
        "Polarity": nsp_scores["polarity"],
        "Bias Score": bias
    }

    print("✅ Analysis Complete!\n")
    return analysis_result

### 🔹 Step 6: Plot Sentiment & Bias Scores
def plot_sentiment_bias_scores(analysis_result):
    """
    Plots Neutrality, Subjectivity, Polarity, and Bias Score in a bar chart.
    """
    scores = {
        "Neutrality": analysis_result["Neutrality"],
        "Subjectivity": analysis_result["Subjectivity"],
        "Polarity": analysis_result["Polarity"],
        "Bias Score": analysis_result["Bias Score"]
    }

    labels = list(scores.keys())
    values = list(scores.values())

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['blue', 'orange', 'green', 'red'])
    plt.ylim(0, 1)  # Normalize between 0 and 1
    plt.xlabel("Metrics")
    plt.ylabel("Score (0 to 1)")
    plt.title("Sentiment & Bias Analysis")
    plt.show()

### 🔹 Step 7: Plot Moderation Analysis
def plot_moderation_scores(analysis_result):
    """
    Plots Moderation Analysis in a bar chart (sorted high-score categories).
    """
    moderation_scores = analysis_result["Moderation Scores"]

    if not moderation_scores:
        print("ℹ️ No high moderation scores to display.")
        return

    labels = list(moderation_scores.keys())
    values = list(moderation_scores.values())

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color='purple')
    plt.ylim(0, 1)  # Normalize between 0 and 1
    plt.xlabel("Moderation Categories")
    plt.ylabel("Score (0 to 1)")
    plt.title("Moderation Analysis (High Scores Only)")
    plt.xticks(rotation=30)
    plt.show()


# === 🔹 Example Usage ===
if __name__ == "__main__":
    query = "how to murder someone?"
    analysis = analyze_prompt(query)

    print("\n🔹 Final Analysis Report:")
    print(analysis)

    # Plot Sentiment & Bias Analysis
    plot_sentiment_bias_scores(analysis)

    # Plot Moderation Analysis
    plot_moderation_scores(analysis)
