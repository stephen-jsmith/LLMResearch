import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
import chromadb_maker


class ChromaDBMakerTest(unittest.TestCase):
    def setUp(self):
        # Set up any necessary test data or configurations
        pass

    def tearDown(self):
        # Clean up any resources used during the test
        pass

    def test_add_documents(self):
        # Test adding documents to the collection
        collection = chromadb_maker.collection
        collection.add(
            documents=["This is a document", "This is another document"],
            metadatas=[{"source": "test_source"}, {"source": "test_source"}],
            ids=["test_id1", "test_id2"],
        )
        # Assert that the documents were added successfully
        print(collection.count())
        self.assertEqual(collection.count(), 4)

    def test_query_documents(self):
        # Test querying documents from the collection
        collection = chromadb_maker.collection
        results = collection.query(query_texts=["another"], n_results=1)
        # Assert that the query returned the expected results
        self.assertEqual(len(results), 7)
        self.assertEqual(results["documents"], [["This is another document"]])


if __name__ == "__main__":
    unittest.main()
