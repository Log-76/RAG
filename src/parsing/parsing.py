from pathlib import Path
from ..utils import error
from typing import Any
import json


class parser():
    @staticmethod
    def load_file(path: Path) -> Any:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            # si data n existe pas alors return de list vide
            if not raw_data:
                error("raw_data not exist")
                return []
            return raw_data
        except Exception as e:
            error(f"error: {e}")
            return []

    @staticmethod
    def parse_json(raw_data: str) -> Any:
        if isinstance(raw_data, dict) and "rag_questions" in raw_data:
            try:
                return
            except Exception as e:
                error(f"error: {e}")
        else:
            return None
