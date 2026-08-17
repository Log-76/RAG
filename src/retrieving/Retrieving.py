from langchain_community.retrievers import BM25Retriever
from indexing import Indexing
from pathlib import Path


class Retrieving():
    def __init__(self, source: Path, k: int = 1):
        self.k: int = k
        self.source: Path = source
        self.docs = Indexing.load(self.source)

    def retrieving(self):

        # Création du retriever BM25
        retriever = BM25Retriever.from_documents(self.docs)
        retriever.k = self.k  # Nombre de résultats à renvoyer

        # Recherche
        results = retriever.invoke("BM25 pertinence")
        return results
