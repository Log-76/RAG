from pydantic import BaseModel, Field
import json


class parser(BaseModel):
    path = Field(..., description="Path to the functions definition JSON file")

    def load_file(self):
        data = list(json.load(self.path))
        print(data)
