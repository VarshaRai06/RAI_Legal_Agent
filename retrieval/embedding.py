import os
import json
import torch
from sentence_transformers import SentenceTransformer
import chromadb  # Using ChromaDB for storing embeddings

# Paths
CHUNKED_DIR = "data/chunks"
VECTOR_DB_DIR = "data/vector_db"

os.makedirs(VECTOR_DB_DIR, exist_ok=True)

# Load the Legal-BERT model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer("nlpaueb/legal-bert-base-uncased").to(device)

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path=VECTOR_DB_DIR)

# Separate collections for Civil & Criminal Laws
civil_law_collection = chroma_client.get_or_create_collection(name="civil_law_rag")
criminal_law_collection = chroma_client.get_or_create_collection(name="criminal_law_rag")

def load_chunked_data(file_path):
    """Loads chunked data from JSON."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def embed_and_store(file_path, collection):
    """Embeds legal text chunks and stores them in the appropriate vector database collection."""
    data = load_chunked_data(file_path)

    for doc_name, chunks in data.items():
        print(f"🔹 Processing {doc_name}...")

        for i, chunk in enumerate(chunks):
            embedding = model.encode(chunk, convert_to_tensor=True).cpu().tolist()
            collection.add(
                ids=[f"{doc_name}_{i}"],
                embeddings=[embedding],
                metadatas=[{"document": doc_name, "chunk_index": i, "text": chunk}]
            )

    print(f"✅ Embeddings stored for {file_path}")

if __name__ == "__main__":
    print("🔹 Embedding Civil Law data...")
    embed_and_store(os.path.join(CHUNKED_DIR, "civil_laws_chunks.json"), civil_law_collection)

    print("🔹 Embedding Criminal Law data...")
    embed_and_store(os.path.join(CHUNKED_DIR, "criminal_laws_chunks.json"), criminal_law_collection)

    print("✅ All embeddings stored successfully in separate collections!")
