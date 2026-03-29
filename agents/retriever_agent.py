from typing import List, Dict

class RetrieverAgent:
    def __init__(self, retriever):
        self.retriever = retriever

    def run(self, query: str):
        docs = self.retriever.retrieve(query)

        results = []
        for doc in docs:
            results.append({
                "content": doc["text"],
                "source": doc["source"],
                "id": doc["id"]
            })

        return results