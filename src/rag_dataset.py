from pydantic import BaseModel
from typing import List
from parsing.answered_question import AnsweredQuestion, UnansweredQuestion


class RagDataset(BaseModel):
    rag_questions: List[AnsweredQuestion | UnansweredQuestion]
