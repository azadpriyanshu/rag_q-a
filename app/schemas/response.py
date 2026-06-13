from pydantic import BaseModel


class SourceResponse(BaseModel):
    title: str
    score: float


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResponse]