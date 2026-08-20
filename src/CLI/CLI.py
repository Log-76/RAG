from pathlib import Path
from ..utils import error
from .tester_public import RetrievalTester
from ..generation.AnswerOrchestrator import AnswerOrchestrator
from ..generation import Generation
from ..retrieving import Retrieving
from ..indexing import Ingestion


class CLI:
    """Command-Line Interface (CLI) for orchestrating the RAG pipeline.

    Exposes core commands for corpus indexing, similarity search,
    LLM answer generation, and recall evaluation.
    """
    def index(self, max_chunk_size: int = 2000,
              raw_dir: Path = Path("data/raw/vllm-0.10.1/"),
              processed_dir: Path = Path("data/processed/")) -> None:
        """Processes and indexes raw files into BM25 search chunks.

        Args:
            max_chunk_size: Maximum character length for each chunk (1-2000).
            raw_dir: Path to the directory containing raw source files.
            processed_dir: Destination path for storing processed index data.

        Raises:
            ValueError: If `max_chunk_size` is not within the valid range.
        """
        try:
            if max_chunk_size <= 0 or max_chunk_size > 2000:
                raise ValueError(f"Invalid max_chunk_size: {max_chunk_size}"
                                 "\nIt must be between 1 and 2000")
            raw_path = Path(raw_dir)
            processed_path = Path(processed_dir)
            if not raw_path.exists() or not raw_path.is_dir():
                print(f"ERROR: invalid directory: {raw_path}")
                return
            processed_path.mkdir(parents=True, exist_ok=True)
            ingestion = Ingestion(max_chunk_size)
            ingestion.run_indexation(raw_path, processed_path)
        except Exception as e:
            error(f"Error: {e}")
            return

    def search(self, query: str,
               k: int) -> None:
        """Performs a top-k lexical search for a single query.

        Args:
            query: The search prompt or question string.
            k: Number of top relevant sources to retrieve (k > 0).

        Raises:
            ValueError: If `k` is less than or equal to zero.
        """
        try:
            if not query:
                error("The query cannot be empty")
                return
            if k <= 0:
                raise ValueError(f"Invalid k value: {k}")
            retrieving = Retrieving(Path("data/processed"), Path("aa"), k)
            result = retrieving.search_query(query, k)
            for source in result.retrieved_sources:
                print(f"{source.file_path} "
                      f"[{source.first_character_index}:"
                      f"{source.last_character_index}]")
        except Exception as e:
            error(f"ERROR: {e}")
            return

    def search_dataset(self, dataset_path: Path,
                       k: int,
                       save_directory: Path) -> None:
        """Runs top-k search across a full JSON dataset of questions.

        Args:
            dataset_path: Path to the input JSON dataset file.
            k: Number of sources to retrieve per question (k > 0).
            save_directory: Destination directory for saving JSON results.

        Raises:
            ValueError: If `k` is less than or equal to zero.
        """
        try:
            if k <= 0:
                raise ValueError(f"Invalid k value: {k}")
            processed_dataset_path = Path(dataset_path)
            process_save_dir = Path(save_directory)
            if (
                not processed_dataset_path.exists()
                or not processed_dataset_path.is_file()
            ):
                error(f"ERROR: invalid directory: {processed_dataset_path}")
                return
            process_save_dir.mkdir(parents=True, exist_ok=True)
            retrieving = Retrieving(Path("data/processed"),
                                    dataset_path,
                                    k)
            result = retrieving.retrieve_all()
            output_path = process_save_dir / processed_dataset_path.name
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.model_dump_json(indent=2))
            print(f"Saved student_search_results to {output_path}")
        except Exception as e:
            error(f"ERROR: {e}")
            return

    def answer(self, query: str,
               k: int) -> None:
        """Generates an LLM answer for a single question given top-k context.

        Args:
            query: The user question.
            k: Number of retrieved context chunks to pass to the model (k > 0).

        Raises:
            ValueError: If `k` is less than or equal to zero.
        """
        try:
            if not query:
                error("The query cannot be empty")
                return
            if k <= 0:
                raise ValueError(f"Traceback: Invalid k value: {k}")
            retrieving = Retrieving(Path("data/processed"), Path("a"), k)
            search_result = retrieving.search_query(query, k)
            generation = Generation()
            answer = generation.generate_answer(search_result)  # MinimalAnswer
            print(f"Question: {answer.question}")
            print(f"Answer: {answer.answer}")
            print("Sources:")
            for source in answer.retrieved_sources:
                print(f"  {source.file_path} "
                      f"[{source.first_character_index}:"
                      f"{source.last_character_index}]")
        except Exception as e:
            error(f"ERROR: {e}")
            return

    def answer_dataset(self, student_search_results_path: Path,
                       save_directory: Path) -> None:
        """Batch-generates LLM answers for a dataset of pre-retrieved queries.

        Args:
            student_search_results_path: Path to the search results JSON file.
            save_directory: Directory path to output the generated JSON.
        """
        try:
            results_path = Path(student_search_results_path)
            save_path = Path(save_directory)
            if not results_path.exists() or not results_path.is_file():
                error(f"ERROR: invalid file: {results_path}")
                return
            generation = Generation()
            orchestrator = AnswerOrchestrator(generation)
            orchestrator.run(results_path, save_path)
        except Exception as e:
            error(f"ERROR: {e}")

    def evaluate(self, student_search_result_path: Path,
                 dataset_path: Path) -> None:
        """Evaluates retrieval Recall metrics against benchmark datasets.

        Args:
            student_search_result_path: File path of student search outputs.
            dataset_path: File path of the ground-truth benchmark dataset.
        """
        try:
            retrieval_tester = RetrievalTester()
            retrieval_tester.run_docs_recall()
            retrieval_tester.run_code_recall()
        except Exception as e:
            error(f"ERROR: {e}")
            return
