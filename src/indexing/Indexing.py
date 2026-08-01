from pathlib import Path
from rank_bm25 import BM25Okapi
from ..parsing import MinimalSource
from ..utils import error
from ..utils.extract_data import retrieve_data_from_minimal_source
import pickle
import re


class Indexing():
    def __init__(self) -> None:
        self.bm25_index: BM25Okapi | None = None
        self.indexed_sources: list[MinimalSource] = []
        self.indexed_texts: list[str] = []

    def tokenize(self, text: str, file_type: str) -> list[str]:
        try:
            if file_type == "py":
                return re.findall(r'\w+', text)
            elif file_type == "md":
                return re.findall(r'\w+', text.lower())
            else:
                raise ValueError(f"Invalid doc type provided: {file_type}")
        except Exception as e:
            error(f"Error tokenizing: {e}")
            return []

    def build_index(self, data: list[MinimalSource]) -> None:
        try:
            texts: list[str] = []
            tokenized_corpus: list[list[str]] = []
            for source in data:
                texts.append(
                    self.retrieve_data_from_minimal_source(source)
                )
            for source, text in zip(data, texts):
                file_type = Path(source.file_path).suffix.lstrip(".")
                tokenized_corpus.append(self.tokenize(text, file_type))

            self.bm25_index = BM25Okapi(tokenized_corpus)
            self.indexed_sources = data
            self.indexed_texts = texts
            print(f"Indexation finished: {len(texts)} chunks indexed")
        except Exception as e:
            error(f"Failed to build index: {e}")

    def save(self, save_dir: Path) -> None:
        """
        Persists the BM25 index, the indexed sources and the
        indexed texts under save_dir, so retrieval can load them
        back without re-indexing the whole corpus.
        """
        try:
            save_dir.mkdir(parents=True, exist_ok=True)
            with open(save_dir / "bm25_index.pkl", "wb") as f:
                pickle.dump(self.bm25_index, f)
            with open(save_dir / "indexed_sources.pkl", "wb") as f:
                pickle.dump(self.indexed_sources, f)
            with open(save_dir / "indexed_texts.pkl", "wb") as f:
                pickle.dump(self.indexed_texts, f)
        except Exception as e:
            error(f"Failed to save index to {save_dir}: {e}")

    def load(self, save_dir: Path) -> None:
        """
        Loads a previously persisted index from save_dir.
        """
        try:
            with open(save_dir / "bm25_index.pkl", "rb") as f:
                self.bm25_index = pickle.load(f)
            with open(save_dir / "indexed_sources.pkl", "rb") as f:
                self.indexed_sources = pickle.load(f)
            with open(save_dir / "indexed_texts.pkl", "rb") as f:
                self.indexed_texts = pickle.load(f)
        except Exception as e:
            error(f"Failed to load index from {save_dir}: {e}")
