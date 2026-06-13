from fastapi import APIRouter, HTTPException
from app.schemas.request import QuestionRequest
from app.schemas.response import QuestionResponse
from app.services.rag_service import RAGService


router = APIRouter()

rag_service = RAGService()


@router.post(
    "/ask",
    response_model=QuestionResponse
)
def ask_question(
    request: QuestionRequest
):

    try:

        result = rag_service.ask(
            question=request.question
        )

        return QuestionResponse(
            question=result["question"],
            answer=result["answer"],
            sources=result["sources"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.post(
    "/ask",
    response_model=QuestionResponse
)
def ask_question(
    request: QuestionRequest
):

    try:

        result = rag_service.ask(
            request.question
        )

        return QuestionResponse(
            question=result["question"],
            answer=result["answer"],
            sources=result["sources"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )