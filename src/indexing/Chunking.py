from ..utils import error
from pathlib import Path
from ..parsing import MinimalSource
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language


class Chunking():
    """
    Chunk a document given the path of this document.
    Supports only .py and .md files, raises an error otherwise.
    """

    def __init__(self, chunk_size: int, file_type: str) -> None:
        """
        chunk_size: size of a chunk
        file_type: extension of the chunked document
        """
        self.chunk_size: int = chunk_size
        self.file_type: str = file_type

    def chunking(self, path: Path) -> list[MinimalSource]:
        """
        Checks the type of document to chunk, supports only
        python and md files, raises an error otherwise.
        Returns an empty list (and logs the error) instead of
        killing the whole indexing run when a single file fails.
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = f.read()
            if self.file_type == "py":
                return self.python_chunking(path, data)
            elif self.file_type == "md":
                return self.text_chunking(path, data)
            else:
                raise ValueError(
                    "Invalid data format: expected python or markdown/text"
                )
        except Exception as e:
            error(f"Failed to chunk {path}: {e}")
            return []

    def text_chunking(self, path: Path, data: str) -> list[MinimalSource]:
        """
        Chunks the data using the .md algo
        """
        overlap: int = self.chunk_size // 6
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=overlap,
            add_start_index=True
        )
        docs = splitter.create_documents([data])
        source = []
        for doc in docs:
            start_index = doc.metadata['start_index']
            end_index = start_index + len(doc.page_content)
            source.append(MinimalSource(file_path=str(path),
                                        first_character_index=start_index,
                                        last_character_index=end_index))
        return source

    def python_chunking(self, path: Path, data: str) -> list[MinimalSource]:
        """
        Chunks the data using the .py algo
        """
        overlap: int = self.chunk_size // 5
        splitter = RecursiveCharacterTextSplitter.from_language(
            chunk_size=self.chunk_size,
            chunk_overlap=overlap,
            language=Language.PYTHON,
            add_start_index=True
        )
        docs = splitter.create_documents([data])
        source = []
        for doc in docs:
            start_index = doc.metadata['start_index']
            end_index = start_index + len(doc.page_content)
            source.append(MinimalSource(file_path=str(path),
                                        first_character_index=start_index,
                                        last_character_index=end_index))
        return source
