import json
import traceback
import os
from pathlib import Path
from typing import Any
from tqdm import tqdm
from ..utils import error
from ..generation.AnswerOrchestrator import AnswerOrchestrator
from ..generation import Generation
from ..retrieving import Retrieving
from ..indexing import Ingestion

class CLI:
    def index(self, max_chunk_size: int = 2000,
              raw_dir: Path = Path("data/raw/vllm-0.10.1/"),
              processed_dir: Path = Path("data/processed/")) -> None:
        try:
            if max_chunk_size <= 0 or max_chunk_size > 2000:
                raise ValueError(f"Invalid max_chunk_size: {chunk_size}"
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
        try:
            if not query:
                error("The query cannot be empty")
                return
            if k <= 0:
                raise ValueError(f"Invalid k value: {k}")
            retrieving = Retrieving("data/processed", "aa", k)
            result = retrieving.search_query(query, k)
            for source in result.retrieved_sources:
                print(f"{source.file_path} [{source.first_character_index}:{source.last_character_index}]")
        except Exception as e:
            error(f"ERROR: {e}")
            return

    def answer_dataset(self, dataset_path: Path,
                       k: int,
                       save_directory: Path) -> None:
        try:
            if k <= 0:
                raise ValueError(f"Invalid k value: {k}")
            processed_dataset_path = Path(dataset_path)
            process_save_dir = Path(save_directory)
            if not processed_dataset_path.exists() or not processed_dataset_path.is_file():
                error(f"ERROR: invalid directory: {processed_dataset_path}")
                return
            process_save_dir.mkdir(parents=True, exist_ok=True)
            retrieving = Retrieving("data/processed",
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
        try:
            if not query:
                error("The query cannot be empty")
                return
            if k <= 0:
                raise ValueError(f"Invalid k value: {k}")
            retrieving = Retrieving("data/processed", "a", k)
            search_result = retrieving.search_query(query, k)
            generation = Generation()
            answer = generation.generate_answer(search_result)  # MinimalAnswer
            print(f"Question: {answer.question}")
            print(f"Answer: {answer.answer}")
            print("Sources:")
            for source in answer.retrieved_sources:
                print(f"  {source.file_path} [{source.first_character_index}:{source.last_character_index}]")
        except Exception as e:
            error(f"ERROR: {e}")
            traceback.print_exc()
            return

    def answer_dataset(self, student_search_results_path: Path,
                       save_directory: Path) -> None:
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
