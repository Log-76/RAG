from pydantic import BaseModel, Field
from utils import error

class MinimalSource(BaseModel):
    file_path: str
    first_character_index: int
    last_character_index: int
