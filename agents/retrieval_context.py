import chromadb
from retrieval.load_collections import get_chroma_collections
from sentence_transformers import SentenceTransformer

# Load embedding model (same as used in Phase 1)
embedding_model = SentenceTransformer("BAAI/bge-base-en")

# Load ChromaDB collections
civil_law_collection, criminal_law_collection = get_chroma_collections()

def retrieve_legal_text(query: str, law_type: str, top_k=5):
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

    # Perform similarity search in ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k  # Retrieve top-k most relevant results
    )

    # Format output
    retrieved_texts = []
    for i in range(len(results["documents"][0])):
        retrieved_texts.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i].get("source", "Unknown Source"),
            "confidence_score": round(100 - (i * (100 / top_k)), 2)  # Assign a confidence score
        })

    

    return retrieved_texts
