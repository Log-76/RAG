from pydantic import BaseModel, Field
import json


class parser(BaseModel):
    path: str = Field(
        ...,
        description="Path to the functions definition JSON file")

    def load_file(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = dict(json.load(f))
            # verif que on a bien une liste d info
            if not isinstance(data, dict):
                print("error is not dict")
                return []
            return data
        except Exception as e:
            print(e)
            return []


c = parser(path="dataset_code_public.json")
print(c.load_file())
