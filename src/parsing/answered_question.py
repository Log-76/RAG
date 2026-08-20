import uuid
from pydantic import BaseModel, Field
from typing import List
from .minimal_source import MinimalSource


class UnansweredQuestion(BaseModel):
    """Represents a dataset question that has not yet been answered.

    Attributes:
        question_id (str): Unique UUID identifier generated automatically.
        question (str): The raw text of the question.
    """
    question_id: str = Field(default_factory=lambda:
                             str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    """Represents a dataset question enriched
    with ground-truth sources and answer.

    Inherits from UnansweredQuestion.

    Attributes:
        sources (List[MinimalSource]): List of source
        references supporting the answer.
        answer (str): The expected ground-truth answer text.
    """
    sources: List[MinimalSource]
    answer: str
