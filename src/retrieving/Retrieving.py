from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document


class Retrieving():
    def __init__(self, k: int = 1):
        self.k: int = k

    def retrieving(self):
        docs = [
            Document(page_content="Le RAG améliore les réponses des LLM."),
            Document(page_content="BM25 calcule la pertinence basée"
                     " sur la fréquence des termes.")
        ]

        # Création du retriever BM25
        retriever = BM25Retriever.from_documents(docs)
        retriever.k = self.k  # Nombre de résultats à renvoyer

        # Recherche
        results = retriever.invoke("BM25 pertinence")
        return results
