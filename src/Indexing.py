from utils import error
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

class  Indexing():
    def __init__(self, chunk_size: int, is_python: bool, is_text: bool) -> None:
        self.chunk_size: int = chunk_size
        self.is_python: bool = is_python
        self.is_text: bool = is_text

    def chunking(self, path: Path, data: list[str]) -> list[MinimalSource]:
        try:
            if self.is_python:
                return self.python_chunking(path, data)
            elif self.is_text:
                return self.text_chunking(path, data)
            else:
                raise Exception("Invalid data format: "
                                "expected python or markdown/text")
        except Exception as e:
            error(e)
            exit()

    def text_chunking(self, path: Path, data: list[str]) -> list[MinimalSource]:
        overlap: int = self.chunk_size // 10
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=overlap,
            add_start_index=True
            )
        docs = splitter.create_documents(data)
        source = []
        for doc in docs:
            start_index = doc.metadata['start_index']
            end_index = start_index + len(doc.page_content)
            source.append(MinimalSource(file_path=path,
                                        first_character_index=start_index,
                                        last_character_index=end_index))
        return source

    def python_chunking(self, path: Path, data: list[str]) -> list[MinimalSource]:
        overlap: int = self.chunk_size // 10
        splitter = RecursiveCharacterTextSplitter.from_language(chunk_size=self.chunk_size,
                                                                chunk_overlap=overlap,
                                                                language=Language.PYTHON,
                                                                add_start_index=True)
        docs = splitter.create_documents(data)
        source = []
        for doc in docs:
            start_index = doc.metadata['start_index']
            end_index = start_index + len(doc.page_content)
            source.append(MinimalSource(file_path=path,
                                        first_character_index=start_index,
                                        last_character_index=end_index))
        return source
