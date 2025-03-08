import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from nltk.translate.meteor_score import meteor_score
import torch
from bert_score import score as bert_score

# Ensure NLTK resources are available
nltk.download('wordnet')

def compute_bleu(reference, candidate):
    """
    Computes BLEU score for a single reference-candidate pair.
    Args:
        reference (str): The retrieved legal text (ground truth).
        candidate (str): The LLM-generated response.
    Returns:
        float: BLEU score (0-1 scale).
    """
    ref_tokens = reference.split()
    cand_tokens = candidate.split()
    smoothie = SmoothingFunction().method4  # Smoothing for better BLEU accuracy
    return sentence_bleu([ref_tokens], cand_tokens, smoothing_function=smoothie)

def compute_rouge(reference, candidate):
    """
    Computes ROUGE scores (ROUGE-1, ROUGE-2, ROUGE-L) between reference and candidate.
    Args:
        reference (str): The retrieved legal text (ground truth).
        candidate (str): The LLM-generated response.
    Returns:
        float: ROUGE-L F1 score (best for long text similarity).
    """
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, candidate)
    return scores['rougeL'].fmeasure  # We return ROUGE-L F1 score

def compute_meteor(reference, candidate):
    """
    Computes METEOR score for a single reference-candidate pair.
    Args:
        reference (str): The retrieved legal text (ground truth).
        candidate (str): The LLM-generated response.
    Returns:
        float: METEOR score (0-1 scale).
    """
    return meteor_score([reference], candidate)

def compute_bert(reference, candidate):
    """
    Computes BERTScore for a single reference-candidate pair.
    Args:
        reference (str): The retrieved legal text (ground truth).
        candidate (str): The LLM-generated response.
    Returns:
        float: BERTScore F1 score.
    """
    P, R, F1 = bert_score([candidate], [reference], lang="en", rescale_with_baseline=True)
    return F1[0].item()  # Extract the F1 score as a float

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


def evaluate_llm_responses(llm_responses, clubbed_reference_text):
    """
    Evaluates each LLM response against the clubbed reference text.

    Args:
        llm_responses (list[dict]): List of LLM-generated responses.
        clubbed_reference_text (str): The combined reference text from retrieved legal contexts.

    Returns:
        list[dict]: List of responses with their respective evaluation scores.
    """
    evaluated_responses = []

    for response_obj in llm_responses:
        response_id = response_obj["response_id"]
        response_text = response_obj["response"]
        response_citations = response_obj["citations"]
        # Compute evaluation scores
        bleu = compute_bleu(clubbed_reference_text, response_text)
        rouge = compute_rouge(clubbed_reference_text, response_text)
        meteor = compute_meteor(clubbed_reference_text, response_text)
        bert = compute_bert(clubbed_reference_text, response_text)

        # Store evaluation results
        evaluated_responses.append({
            "response_id": response_id,
            "response": response_text,
            "citations": response_citations,
            "bleu_score": bleu,
            "rouge_score": rouge,
            "meteor_score": meteor,
            "bert_score": bert,
            "final_score": (0.25 * bleu + 0.25 * rouge + 0.25 * meteor + 0.25 * bert)  # Weighted average
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
def process_evaluation(llm_responses, retrieved_texts):
    """
    Orchestrates the entire evaluation process when called by another agent.

    Args:
        llm_responses (list[dict]): List of LLM-generated responses.
        retrieved_texts (list[dict]): List of retrieved legal text chunks.

    Returns:
        list[dict]: Top-ranked responses ready for fact-checking.
    """
    # Step 1: Club top 2 retrieved texts into a single reference text
    clubbed_reference_text = club_top_retrieved_texts(retrieved_texts)

    # Step 2: Evaluate all LLM responses against this reference text
    evaluated_responses = evaluate_llm_responses(llm_responses, clubbed_reference_text)

    # Step 3: Rank responses and select the top 2
    top_responses = select_top_responses(evaluated_responses)

    return top_responses  # This goes to the Fact-Checking Agent
