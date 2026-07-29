from pydantic import BaseModel


class MinimalSource(BaseModel):
    file_path: str
    first_character_index: int
    last_character_index: int

    def data(self):
        return {"file_path": self.file_path,
                "first_character_index": self.first_character_index,
                "last_character_index": self.last_character_index}
