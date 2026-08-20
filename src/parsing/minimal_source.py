from pydantic import BaseModel


class MinimalSource(BaseModel):
    """Represents a specific source chunk location within a file.

    Attributes:
        file_path (str): Relative path to the referenced file.
        first_character_index (int): Starting character index of the chunk.
        last_character_index (int): Ending character index of the chunk.
    """
    file_path: str
    first_character_index: int
    last_character_index: int
