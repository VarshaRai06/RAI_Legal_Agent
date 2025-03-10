import chromadb


def get_chroma_collections():
    """
    Connects to ChromaDB and loads the stored collections for Civil Law & Criminal Law.
    """
    # Initialize ChromaDB client (persistent storage)
    client = chromadb.PersistentClient(path="data/vector_db")

    # Load collections
    civil_law_collection = client.get_or_create_collection("civil_law_rag")
    criminal_law_collection = client.get_or_create_collection("criminal_law_rag")
    print("civil_law_collection loaded")

    

    return civil_law_collection, criminal_law_collection


