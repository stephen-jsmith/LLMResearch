import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
import os
import pandas as pd
from data_frame_vectorizer import count_tokens, compute_doc_embeddings, vectorize_data
from sentence_transformers import SentenceTransformer


class TestDataFrameVectorizer(unittest.TestCase):
    def test_count_tokens(self):
        text = "This is a sample text."
        expected_tokens = 6

        tokens = count_tokens(text)

        self.assertEqual(tokens, expected_tokens)

    def test_compute_doc_embeddings(self):
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        df = pd.DataFrame(
            {
                "content": ["This is a sample text.", "Another sample text."],
            }
        
        )
        expected_embeddings = model.encode(df["content"])

        embeddings = compute_doc_embeddings(df)

        self.assertEqual(embeddings, expected_embeddings)

    def test_vectorize_data(self):
        input_dir = "md_files"
        output_dir = "vectorized_dataframes"
        expected_filenames = ["file1.md", "file2.md"]

        ret_list, filenames = vectorize_data(input_dir, output_dir)

        self.assertEqual(filenames, expected_filenames)
        self.assertIsInstance(ret_list, list)
        self.assertIsInstance(ret_list[0], pd.DataFrame)


if __name__ == "__main__":
    unittest.main()
