import chromadb
import torch
from retrieval.load_collections import get_chroma_collections
from sentence_transformers import SentenceTransformer, models

# Load embedding model (same as used in Phase 1)
word_embedding_model = models.Transformer("nlpaueb/legal-bert-base-uncased", max_seq_length=512)
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(), pooling_mode_mean_tokens=True)

# Combine into a SentenceTransformer model
# embedding_model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
embedding_model = SentenceTransformer("BAAI/bge-m3")
# Debug: Confirm Model Components
print("✅ BAAI/bge-m3 Loaded with Custom Pooling!")

# Load ChromaDB collections
civil_law_collection, criminal_law_collection = get_chroma_collections()

def retrieve_legal_text(query: str, law_type: str, top_k=3):
    """
    Retrieves the most relevant legal text from ChromaDB based on the query.

    Args:
        query (str): The user's legal question.
        law_type (str): "general_law" for Family + Civil Law, "criminal_law" for Criminal Law.
        top_k (int): Number of relevant chunks to retrieve.

    Returns:
        list[dict]: List of retrieved legal text chunks with metadata.
    """
    # Select correct collection
    if law_type == "civil_law":
        collection = civil_law_collection
    elif law_type == "criminal_law":
        collection = criminal_law_collection
    elif law_type == "both":
        collection = civil_law_collection
        collection = criminal_law_collection
    else:
        raise ValueError("Invalid law type! Choose 'civil_law' or 'criminal_law'.")

    # Convert query into embedding
    
    query_embedding = embedding_model.encode(query, convert_to_tensor=True).tolist()

    # Debugging: Print Query Embedding
    # print("✅ Query Embedding Shape:", len(query_embedding))
    # print("✅ Query Embedding Sample Values:", query_embedding[:10])  # Print first 10 values


    # Perform similarity search in ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k  # Retrieve top-k most relevant results
    )
    
    # print("✅ Raw ChromaDB Query Results:", results)
    
    # Format output
    retrieved_texts = []
    for i in range(len(results["metadatas"][0])):
        retrieved_texts.append({
            "text": results["metadatas"][0][i].get("text", "No text found"),
            # "source": results["metadatas"][0][i].get("source", "Unknown Source"),
            # "confidence_score": round(100 - (i * (100 / top_k)), 2)  # Assign a confidence score
        })

    
    print("✅ Retrieval complete")

    return retrieved_texts
