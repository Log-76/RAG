import re
import uuid
from ..indexing import Indexing
from pathlib import Path
from ..utils.utils import error
from ..minimal_search_results import MinimalSearchResults
from ..student_search import StudentSearchResults
from ..parsing.parsing import parser


class Retrieving():
    def __init__(self, source: Path, question_path: Path, k: int = 1):
        self.source: Path = source
        self.docs = Indexing()
        self.docs.load(Path(self.source))
        self.question_path = Path(question_path)
        self.k = k

    def retrieve_all(self) -> StudentSearchResults:
        data = parser.load_file(self.question_path)
        questions_list = data.get("rag_questions", [])

        all_results = []
        for item in questions_list:
            q_id = item["question_id"]
            q_text = item["question"]

            # Appel de la recherche pour la question en cours
            result = self.retrieving(question_id=q_id, question=q_text)
            if result:
                all_results.append(result)

        return StudentSearchResults(search_results=all_results, k=self.k)

    def retrieving(self, question_id, question: str) -> MinimalSearchResults:
        try:
            if not self.docs.bm25_index:
                error("L'index BM25 not exist")
            # decoupage de la question part mot
            # lower pour metre tout en miniscule
            # Utilise re.findall pour extraire uniquement les mots/identifiants
            tokenized_query = re.findall(r'\w+', question.lower())

            # Création du retriever BM25
            retrieving = self.docs.bm25_index.get_top_n(tokenized_query,
                                                        self.docs.
                                                        indexed_sources,
                                                        n=self.k)
            results = MinimalSearchResults(question_id=question_id,
                                           question=question,
                                           retrieved_sources=retrieving)
            return results
        except Exception as e:
            error(f"error: {e}")

    def search_query(self, query: str, k: int):
        try:
            if not self.docs.bm25_index:
                error("L'index BM25 not exist")
            tokenized_query = re.findall(r'\w+', query.lower())

            retrieving = self.docs.bm25_index.get_top_n(tokenized_query,
                                                        self.docs.
                                                        indexed_sources,
                                                        n=k)
            # generatiomn de l id
            query_id = str(uuid.uuid4())

            result = MinimalSearchResults(question_id=query_id,
                                          question=query,
                                          retrieved_sources=retrieving)
            return result
        except Exception as e:
            error(f"error: {e}")
            return
