import os
import json
import torch
import shutil
from sentence_transformers import SentenceTransformer, models
import chromadb  # Using ChromaDB for storing embeddings

# Delete the entire ChromaDB directory (Wipe all stored data)
shutil.rmtree("data/vector_db")
print("vector db removed")

# Paths
CHUNKED_DIR = "data/chunks"
VECTOR_DB_DIR = "data/vector_db"

os.makedirs(VECTOR_DB_DIR, exist_ok=True)

# Force SentenceTransformer to use Legal-BERT with pooling
word_embedding_model = models.Transformer("nlpaueb/legal-bert-base-uncased", max_seq_length=512)
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(), pooling_mode_mean_tokens=True)

# Combine Transformer + Pooling into SentenceTransformer
# embedding_model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
# Load BGE-M3 (Optimized for retrieval)
embedding_model = SentenceTransformer("BAAI/bge-m3")

print("✅ BAAI/bge-m3 Model for Chunk Embeddings Loaded with Custom Pooling!")

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path=VECTOR_DB_DIR)

# Delete corrupted embeddings
# print("Deleting collections")
# chroma_client.delete_collection("civil_law_rag")
# print("Deleted collection civil")
# chroma_client.delete_collection("criminal_law_rag")
# print("Deleted collection criminal")

# Separate collections for Civil & Criminal Laws
civil_law_collection = chroma_client.get_or_create_collection(name="civil_law_rag", metadata={"hnsw:space": "cosine", "index_type": "IVF_FLAT"})
criminal_law_collection = chroma_client.get_or_create_collection(name="criminal_law_rag", metadata={"hnsw:space": "cosine", "index_type": "IVF_FLAT"})

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
            embedding = embedding_model.encode(chunk, convert_to_tensor=True).cpu().tolist()
            collection.add(
                ids=[f"{doc_name}_{i}"],
                embeddings=[embedding],
                metadatas=[{"document": doc_name, "chunk_index": i, "text": chunk}]
            )
            if i < 3:  # Print first 3 embeddings
                print(f"✅ Chunk {i} Embedding (First 10 Values):", embedding[:10])

    print(f"✅ Embeddings stored for {file_path}")

if __name__ == "__main__":


    print("🔹 Embedding Civil Law data...")
    embed_and_store(os.path.join(CHUNKED_DIR, "civil_laws_chunks.json"), civil_law_collection)

    print("🔹 Embedding Criminal Law data...")
    embed_and_store(os.path.join(CHUNKED_DIR, "criminal_laws_chunks.json"), criminal_law_collection)

    print("✅ All embeddings stored successfully in separate collections!")
