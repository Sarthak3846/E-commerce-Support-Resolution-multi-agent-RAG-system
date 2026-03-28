from typing import List, Dict

class RetrieverAgent:
    def __init__(self, retriever):
        self.retriever = retriever

    def run(self, query: str) -> List[Dict]:
        docs = self.retriever.get_relevant_documents(query)

        results = []
        for doc in docs:
            results.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
                "section": doc.metadata.get("section", "N/A")
            })

        return results