from fastapi import APIRouter

from app.api.v1.endpoints.ask import (
    router as ask_router
)
from app.api.v1.endpoints.health import (
    router as health_router
)

api_router = APIRouter()

api_router.include_router(
    ask_router,
    tags=["RAG"]
)



api_router.include_router(
    health_router,
    tags=["Health"]
)