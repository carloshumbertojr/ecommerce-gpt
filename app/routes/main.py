from fastapi import APIRouter

from app.routes import answer, question

api_router = APIRouter()

api_router.include_router(answer.router, prefix="/answer", tags=["answer"])
api_router.include_router(question.router, prefix="/questions", tags=["questions"])
