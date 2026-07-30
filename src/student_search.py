from pydantic import BaseModel
from typing import List
from minimal_search_results import MinimalSearchResults, MinimalAnswer


class StudentSearchResults(BaseModel):
    search_results: List[MinimalSearchResults]
    k: int


class StudentSearchResultsAndAnswer(BaseModel):
    search_results: List[MinimalAnswer]
    k: int
