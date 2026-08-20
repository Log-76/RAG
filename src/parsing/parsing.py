from pathlib import Path
from ..utils import error
from typing import Any
import json


class parser():
    """Utility class for loading and validating JSON files and structures.

    Provides static methods to read files safely
    and extract RAG question datasets.
    """
    @staticmethod
    def load_file(path: Path) -> Any:
        """Loads and parses a JSON file from disk safely.

        Args:
            path: Path object pointing to the target JSON file.

        Returns:
            Parsed JSON content (dict or list), or an empty list
            if loading fails or data is empty.
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            if not raw_data:
                error("raw_data not exist")
                return []
            return raw_data
        except Exception as e:
            error(f"error: {e}")
            return []

    @staticmethod
    def parse_json(raw_data: str) -> Any:
        """Validates whether raw data contains a valid
        RAG question dataset structure.

        Args:
            raw_data: The data structure (usually a dictionary) to validate.

        Returns:
            The raw data if valid, or
            None if validation fails or key is missing.
        """
        if isinstance(raw_data, dict) and "rag_questions" in raw_data:
            try:
                return
            except Exception as e:
                error(f"error: {e}")
        else:
            return None
