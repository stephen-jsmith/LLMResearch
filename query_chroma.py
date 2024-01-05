import chromadb
from chromadb.config import Settings

chroma_client = chromadb.PersistentClient(path="./chroma_save_states")


collection = chroma_client.get_collection("testing")

print(collection.query(query_texts=["What is Abaca?"], n_results=5))
