from pydantic import BaseModel, Field
import json


class parser(BaseModel):
    path: str = Field(
        ...,
        description="Path to the functions definition JSON file")

    def load_file(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(data)
        except Exception as e:
            print(e)


c = parser(path="dataset_code_public.json")
c.load_file()
