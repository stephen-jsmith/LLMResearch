# Import Statements
import pandas as pd
import chromadb

FILENAME = 'vectorizedDataFrames/apps.csv'

# Create the chroma client, collection for data
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="Testing")


# Load the data
df = pd.read_csv(FILENAME)

collection.add(
    embeddings = df['vector_embedding'].to_list(),
    ids = df['content'].to_list()
    )

results = collection.query(
    query_texts = df['content'].to_list()[3],
    n_results = 3
)