# Import Statements
import pandas as pd
import chromadb
import markdown2
from bs4 import BeautifulSoup
from transformers import GPT2TokenizerFast
import numpy as np
import openai
from openai import OpenAI
import os
import pickle
import numpy as np
from nltk.tokenize import sent_tokenize
import glob
from data_frame_vectorizer import vectorize_data

FILENAME = "vectorized_dataframes/apps.csv"

# Create the chroma client, collection for data
chroma_client = chromadb.PersistentClient(
    path="C:\\Users\\Stephen\\LLMResearch\\chromaSaveStates"
)
collection = chroma_client.get_or_create_collection(name="Testing1")


# Load the data
df = pd.read_csv(FILENAME)

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
