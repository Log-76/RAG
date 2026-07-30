import uuid
from pydantic import BaseModel, Field
from typing import List
from parsing.minimal_source import MinimalSource


class UnansweredQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda:
                             str(uuid.uuid4()))
    question: str

    def UnansweredQuestion_data(self):
        return {"question_id": self.question_id, "question": self.question}


class AnsweredQuestion(UnansweredQuestion):
    sources: List[MinimalSource]
    answer: str
