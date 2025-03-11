import nltk
import shutil
import os, re
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
# from nltk.tokenize import word_tokenize
from nltk.translate.meteor_score import meteor_score
import torch
from bert_score import score as bert_score

# ✅ Step 1: Remove ALL NLTK Data to Fix Corrupt Files
for path in nltk.data.path:
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)

# ✅ Step 2: Reinstall NLTK Resources Cleanly
# nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

print("✅ NLTK Reinstalled Successfully")

def custom_tokenize(text):
    """
    Uses regex-based tokenization instead of NLTK's word_tokenize().
    This avoids dependency on external NLTK resources like 'punkt'.
    """
    return re.findall(r'\b\w+\b', text.lower())  # Extracts words while ignoring punctuation


def compute_bleu(reference_tokens, hypothesis_tokens):
    """
    Computes BLEU score between reference and hypothesis text.
    Args:
        reference_tokens (list[list[str]]): List of tokenized reference texts.
        hypothesis_tokens (list[str]): Tokenized hypothesis text.
    Returns:
        float: BLEU score.
    """
    smoothie = SmoothingFunction().method1  # Prevents zero scores for short texts
    return sentence_bleu(reference_tokens, hypothesis_tokens, smoothing_function=smoothie)


def compute_rouge(reference_tokens, hypothesis_tokens):
    """
    Computes ROUGE score between reference and hypothesis text.
    
    Args:
        reference_tokens (list[list[str]]): Tokenized reference texts.
        hypothesis_tokens (list[str]): Tokenized hypothesis text.

    Returns:
        float: ROUGE-L score.
    """
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)  # ✅ Fixed metric name

    # ✅ Convert Tokenized Lists Back to Strings
    reference_text = " ".join(reference_tokens[0])  # Convert first reference list to string
    hypothesis_text = " ".join(hypothesis_tokens)  # Convert hypothesis tokens to string

    scores = scorer.score(reference_text, hypothesis_text)  # ✅ Ensure both inputs are strings
    return scores["rougeL"].fmeasure  # ✅ Return ROUGE-L F1 Score

def compute_meteor(reference_tokens, hypothesis_tokens):
    """
    Computes METEOR score for a tokenized reference-candidate pair.
    
    Args:
        reference_tokens (list[list[str]]): List of tokenized reference texts.
        hypothesis_tokens (list[str]): Tokenized hypothesis text.

    Returns:
        float: METEOR score (0-1 scale).
    """
    # # ✅ Convert Tokenized Lists Back to Strings
    # reference_text = " ".join(reference_tokens[0])  # Convert first reference list to string
    # hypothesis_text = " ".join(hypothesis_tokens)  # Convert hypothesis tokens to string

    return meteor_score(reference_tokens, hypothesis_tokens)  # ✅ Ensure METEOR gets strings

def compute_bert(reference_tokens, hypothesis_tokens):
    """
    Computes BERTScore for a tokenized reference-candidate pair.
    
    Args:
        reference_tokens (list[list[str]]): List of tokenized reference texts.
        hypothesis_tokens (list[str]): Tokenized hypothesis text.

    Returns:
        float: BERTScore F1 score.
    """
    # ✅ Convert Tokenized Lists Back to Strings
    reference_text = " ".join(reference_tokens[0])  # Convert first reference list to string
    hypothesis_text = " ".join(hypothesis_tokens)  # Convert hypothesis tokens to string

    P, R, F1 = bert_score([hypothesis_text], [reference_text], lang="en", rescale_with_baseline=True)
    return F1[0].item()  # ✅ Ensure BERTScore gets strings

def club_top_retrieved_texts(retrieved_texts):
    """
    Extracts and clubs the top 2 retrieved legal texts into a single reference text.

    Args:
        retrieved_texts (list[dict]): List of retrieved legal text chunks.

    Returns:
        str: Clubbed reference text containing top 2 retrieved legal contexts.
    """
    # Extract only the "text" field from the top 2 retrieved results
    top_texts = [doc["text"] for doc in retrieved_texts[:2]]

    # Combine the texts into one reference passage for evaluation
    clubbed_reference_text = "\n\n".join(top_texts)

    return clubbed_reference_text




# nltk.download("punkt")  # Ensure tokenization is available

def evaluate_llm_responses(llm_responses, clubbed_reference_text):
    """
    Evaluates each LLM response against the clubbed reference text.
    """
    evaluated_responses = []

    # ✅ Tokenize Reference Text
    tokenized_references = [custom_tokenize(clubbed_reference_text)]

    for response_obj in llm_responses:
        response_id = response_obj["response_id"]
        response_text = response_obj["response"]
        response_citations = response_obj.get("citations", [])

        if not response_text.strip():
            evaluated_responses.append({
                "response_id": response_id,
                "response": response_text,
                "citations": response_citations,
                "bleu_score": 0,
                "rouge_score": 0,
                "meteor_score": 0,
                "bert_score": 0,
                "final_score": 0
            })
            continue

        # ✅ Tokenize LLM Response
        tokenized_hypothesis = custom_tokenize(response_text)

        # ✅ Compute Evaluation Scores
        bleu = compute_bleu(tokenized_references, tokenized_hypothesis)
        rouge = compute_rouge(tokenized_references, tokenized_hypothesis)
        meteor = compute_meteor(tokenized_references, tokenized_hypothesis)  # ✅ Fix applied
        bert = compute_bert(tokenized_references, tokenized_hypothesis)  # ✅ Fix applied

        # ✅ Store Evaluation Results
        evaluated_responses.append({
            "response_id": response_id,
            "response": response_text,
            "citations": response_citations,
            "bleu_score": bleu,
            "rouge_score": rouge,
            "meteor_score": meteor,
            "bert_score": bert,
            "final_score": (0.25 * bleu + 0.25 * rouge + 0.25 * meteor + 0.25 * bert)
        })

    return evaluated_responses




def select_top_responses(evaluated_responses, top_k=2):
    """
    Selects the top K best LLM responses based on evaluation scores.

    Args:
        evaluated_responses (list[dict]): List of responses with evaluation scores.
        top_k (int): Number of top responses to return (default is 2).

    Returns:
        list[dict]: Top-ranked responses including citations.
    """
    # Sort responses in descending order based on final score
    sorted_responses = sorted(evaluated_responses, key=lambda x: x["final_score"], reverse=True)

    # Select top K responses
    top_responses = sorted_responses[:top_k]

    # Return structured output with citations
    return [
        {
            "response_id": resp["response_id"],
            "response": resp["response"],
            "citations": resp.get("citations", []),  # Ensure citations are passed forward
            "final_score": resp["final_score"]
        }
        for resp in top_responses
    ]

#this method to be called by the LLM Agent
def process_evaluation( llm_response, retrieved_texts):
    print("Reached evaluation agent")
    """
    Orchestrates the entire evaluation process when called by another agent.

    Args:
        llm_responses (list[dict]): List of LLM-generated responses.
        retrieved_texts (list[dict]): List of retrieved legal text chunks.

    Returns:
        list[dict]: Top-ranked responses ready for fact-checking.
    """
    # retrieved_texts = data.get("retrieved_texts")
    # llm_response = data.get("llm_response")
    # query = data.get("query")

    # Step 1: Club top 2 retrieved texts into a single reference text
    clubbed_reference_text = club_top_retrieved_texts(retrieved_texts)

    # Step 2: Evaluate all LLM responses against this reference text
    evaluated_responses = evaluate_llm_responses(llm_response, clubbed_reference_text)
    print("evaluated_responses <<<```>>>", evaluated_responses)

    # Step 3: Rank responses and select the top 2
    top_responses = select_top_responses(evaluated_responses)
    print("top_responses", top_responses)
    print("reached the end of evaluation agent")

    return top_responses, clubbed_reference_text
    # return {"query":query,"retrieved_texts": retrieved_texts, "top_responses": top_responses, "evaluation_scores": evaluated_responses, "llm_response" : llm_response}  # This goes to the Fact-Checking Agent