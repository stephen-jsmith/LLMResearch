import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
import pandas as pd
from chromadb import PersistentClient
from chroma_add_data import add_data_pandas


class TestChromaAddData(unittest.TestCase):
    def setUp(self):
        self.client = PersistentClient(path="./chroma_save_states")
        self.collection_name = "testing"

    def tearDown(self):
        pass

    def test_add_data_pandas(self):
        # Create a sample dataframe
        df = pd.DataFrame(
            {
                "Question": ["What is Abaca?"],
                "Answer": ["Abaca is a type of banana native to the Philippines."],
            }
        )

        # Call the add_data_pandas function
        add_data_pandas(df, "test_file", self.client, self.collection_name)

        # Retrieve the collection
        collection = self.client.get_collection(self.collection_name)

        # Query the collection to check if the data was added successfully
        results = collection.query(query_texts=["What is Abaca?"], n_results=5)

        # Assert that the query returned the expected result
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]["Answer"], "Abaca is a type of banana native to the Philippines."
        )


if __name__ == "__main__":
    unittest.main()
