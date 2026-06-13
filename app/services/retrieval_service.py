from app.repositories.vector_repository import (
    VectorRepository
)


class RetrievalService:

    def __init__(self):

        self.repo = VectorRepository()

    def retrieve(
        self,
        question: str,
        top_k: int = 5
    ):

        return self.repo.search(
               query=question,
               top_k=top_k
    )