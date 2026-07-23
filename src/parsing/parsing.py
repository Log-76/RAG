from pydantic import BaseModel, Field
from utils import error
import json


class parser(BaseModel):
    path: str = Field(
        ...,
        description="Path to the functions definition JSON file")

    def load_file(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
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
        if "rag_questions" in raw_data:
            rag_questions = dict(raw_data)
            return rag_questions


    # def load_file(self):
    # try:
    #     with open(self.path, 'r', encoding='utf-8') as f:
    #         data = dict(json.load(f))
    #     # verif que on a bien une liste d info
    #     if not isinstance(data, dict):
    #         print("error is not dict", data)
    #         return []
    #     return data
    # except Exception as e:
    #     print(e)
    #     return []


c = parser(path="dataset_code_public.json")
print(c.load_file())
