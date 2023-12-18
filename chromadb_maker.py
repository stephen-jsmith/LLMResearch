# Import Statements
import pandas as pd
import chromadb
from chromadb.config import Settings


# Create the chroma client, collection for data
chroma_client = chromadb.Client(
    Settings(persist_directory="chromaSaveStates")
)
collection = chroma_client.get_or_create_collection(name="Testing1")


collection.add(
    documents=["This is a document", "This is another document"],
    metadatas=[{"source": "my_source"}, {"source": "my_source"}],
    ids=["id1", "id2"],
)

"""collection.add(
    embeddings = df['vector_embedding'].to_list(),
    documents = df['content'].to_list(),
    #ids = 
    )

results = collection.query(
    query_texts = df['content'].to_list()[3],
    n_results = 3
)
"""
results = collection.query(query_texts=["another"], n_results=1)
print(results)
