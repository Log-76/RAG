import json
import os
from pathlib import Path
from typing import Any
from tqdm import tqdm
from ..utils import error
from ..indexing import Ingestion

class CLI:
    def index(self, chunk_size: int = 2000,
              raw_dir: Path = data/raw,
              processed_dir: Path = data/processed) -> None:
        try:
            if chunk_size <= 0 or chunk_size > 2000:
                raise ValueError(f"Invalid chunk_size: {chunk_size}"
                                 "\nIt must be between 1 and 2000")
            raw_path = Path(raw_dir)
            processed_path = Path(processed_dir)
            if not raw_path.exists() or not raw_path.is_dir():
                print(f"ERROR: invalid directory: {raw_path}")
                return
            processed_path.mkdir(parents=True, exist_ok=True)
            ingestion = Ingestion(chunk_size)
            ingestion.run_indexation(raw_path, processed_path)
        except Exception as e:
            error(f"Error: {e}")
            return

    def search(self, raw_data_path: Path,
               k: int,
               raw_save_path: Path) -> None:
        try:
            data_path = Path(raw_data_path)
            save_path = Path(raw_save_path)
            if k <= 0:
                raise ValueError(f"Invalid k value: {k}")
            if not data_path.exists() and not raw_path.is_dir():
                error(f"ERROR: invalid directory: {raw_path}")
                return
        except Exception as e:
            error(f"ERROR: {e}")
            return

    def answer_dataset(self, raw_search_result_path: Path,
                       raw_save_directory: Path) -> None:
        try:
            result_path = Path(raw_result_path)
            search_save_directory = Path(raw_search_directory)
            if not result_path.exists() or not result_path.is_dir():
                error(f"ERROR: invalid directory: {raw_search_result_path}")
        except Exception as e:
            error(f"ERROR: {e}")
            return
