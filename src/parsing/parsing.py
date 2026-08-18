from pydantic import BaseModel, Field
from pathlib import Path
#from .rag_dataset import RagDataset
from ..utils import error, warning
import json


class parser(BaseModel):
    path: str = Field(
        ...,
        description="Path to the functions definition JSON file")

    def load_file(path: Path):
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

    def parse_json(self, raw_data):
        if isinstance(raw_data, dict) and "rag_questions" in raw_data:
            try:
                # return RagDataset.model_validate(raw_data)
                return
            except Exception as e:
                error(f"error: {e}")
        else:
            return None

    def extend_file(self):
        try:
            if "." in self.path:
                stock = self.path.split(".")
                return stock[-1]
        except Exception as e:
            error(e)
        return

    def max_chunks(self, max_chunk=2000):
        if not isinstance(max_chunk, int):
            warning("is not int, value default is 2000")
            return 2000

        if max_chunk > 2000 or max_chunk <= 0:
            max_chunk = 2000
        return max_chunk
