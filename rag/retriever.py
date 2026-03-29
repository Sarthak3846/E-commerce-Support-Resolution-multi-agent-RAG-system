import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

INDEX_PATH = os.path.join(BASE_DIR, "vector_store", "faiss_index.bin")
METADATA_PATH = os.path.join(BASE_DIR, "vector_store", "metadata.json")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K = 4


class Retriever:
    def __init__(self):
        self.index = faiss.read_index(INDEX_PATH)

        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        self.model = SentenceTransformer(MODEL_NAME)

    def embed_query(self, query):
        return self.model.encode([query], convert_to_numpy=True)

    def retrieve(self, query, k=TOP_K):
        query_vector = self.embed_query(query)

        distances, indices = self.index.search(query_vector, k)

        results = []

        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results