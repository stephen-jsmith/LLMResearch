import chromadb
import pandas as pd
import os
from chromadb.config import Settings
import markdown2
from bs4 import BeautifulSoup
from transformers import GPT2TokenizerFast
import numpy as np
import openai
from openai import OpenAI
import pickle
import numpy as np
from nltk.tokenize import sent_tokenize
import glob
from data_frame_vectorizer import vectorize_data
from chromadb.utils import embedding_functions

# Define embedding function
ef = embedding_functions.DefaultEmbeddingFunction()


# Add data straight from a dataframe
def add_data_pandas(
    df: pd.DataFrame,
    filename: str,
    client: chromadb.PersistentClient,
    collection_name: str,
):
    """Add data to the database from a pandas dataframe

    Args:
        df (pd.DataFrame): Dataframe to add to the database
        filename (str): Name of the file
        client (chromadb.PersistentClient): Chroma client
        collection_name (str): Name of the collection to add the data to
    """

    # Verify there is data to add
    if not list(df.index.values):
        print(
            f"*****************\n{filename} is empty, please check to verify data\n*****************"
        )
        return
    collection = client.get_or_create_collection(
        name=collection_name, embedding_function=ef
    )
    if "heading" in df.columns:
        meta = []
        for i in df["heading"]:
            meta.append({filename: i})
    else:
        meta = []
        for i in range(len(df.index)):
            meta.append({filename: "i"})

    collection.add(
        documents=df["content"].tolist(),
        metadatas=meta,
        ids=[filename + str(i) for i in list(df.index.values)],
    )
    print(f"{filename} has been added to the Database!")
    return


if __name__ == "__main__":
    # The following is an example of how to use the add_data_pandas function
    chroma_client = chromadb.PersistentClient(path="./chroma_save_states")

    vector_dataframes, filenames = vectorize_data("md_files", "vectorized_dataframes")
    for i in range(len(vector_dataframes)):
        add_data_pandas(vector_dataframes[i], filenames[i], chroma_client, "testing")

    collection = chroma_client.get_collection("testing")
    collection.query(query_texts=["What is Abaca?"], n_results=5)
