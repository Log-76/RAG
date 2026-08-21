from pathlib import Path
from tqdm import tqdm
from ..parsing import MinimalSource
from .Chunking import Chunking
from .Indexing import Indexing
from ..utils import error


class Ingestion():
    """
    Orchestrates the full indexing pipeline: walk the raw corpus,
    chunk every supported file, build the BM25 index and persist it.
    """

    SUPPORTED_EXTENSIONS: tuple[str, ...] = ("py", "md")

    def __init__(self, max_chunk_size: int) -> None:
        """
        max_chunk_size: max size (in characters) of a single chunk,
        forwarded to the Chunking strategy for every file.
        """
        self.max_chunk_size: int = max_chunk_size
        self.indexer: Indexing = Indexing()

    def collect_files(self, root: Path) -> list[Path]:
        """
        Walks root and returns every file matching a supported
        extension (.py, .md). Returns an empty list (and logs the
        error) if root cannot be scanned.
        """
        try:
            return [
                p for p in root.rglob("*")
                if p.is_file()
                and p.suffix.lstrip(".") in self.SUPPORTED_EXTENSIONS
            ]
        except Exception as e:
            error(f"Failed to walk {root}: {e}")
            return []

    def chunk_files(self, files: list[Path]) -> list[MinimalSource]:
        """
        Chunks every file in files, using the strategy matching its
        extension, and returns the concatenated list of sources.
        A file that fails to chunk is skipped, not fatal.
        """
        all_sources: list[MinimalSource] = []
        for path in tqdm(files, desc="Chunking", unit="file"):
            file_type = path.suffix.lstrip(".")
            chunker = Chunking(
                chunk_size=self.max_chunk_size,
                file_type=file_type
            )
            sources = chunker.chunking(path)
            all_sources.extend(sources)
        return all_sources

    def run_indexation(self, raw_dir: Path, processed_dir: Path) -> None:
        """
        Runs the full ingestion pipeline:
        collect files -> make paths relative -> chunk -> build index -> persist under
        processed_dir.
        """
        files = self.collect_files(raw_dir)
        if not files:
            error(f"No supported files found under {raw_dir}")
            return
        cwd = Path.cwd()
        relative_files: list[Path] = []
        for f in files:
            try:
                relative_files.append(f.relative_to(cwd))
            except ValueError:
                relative_files.append(f)

        all_sources = self.chunk_files(relative_files)
        if not all_sources:
            error("Chunking produced no sources, aborting indexing")
            return

        self.indexer.build_index(all_sources)
        self.indexer.save(processed_dir)
        print(
            f"Ingestion complete! Indexed {len(all_sources)} chunks "
            f"under {processed_dir}/"
        )
