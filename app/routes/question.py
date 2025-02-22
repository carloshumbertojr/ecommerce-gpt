from typing import Any
from fastapi import APIRouter

from app.config.deps import SessionDep
from app.models.question import (
    QuestionCreate,
    QuestionPublic,
    QuestionUpdate,
)
from app.controllers.question import (
    create_question_controller,
    delete_question_controller,
    read_question_controller,
    update_question_controller,
)

router = APIRouter()


@router.post("/", response_model=None)
def create_question_endpoint(
    *,
    session: SessionDep,
    question_in: QuestionCreate,
) -> Any:
    return create_question_controller(session, question_in)


@router.get("/{id}", response_model=QuestionPublic)
def read_question_endpoint(session: SessionDep, id: int) -> Any:
    return read_question_controller(session, id)


@router.put("/{id}", response_model=QuestionPublic)
def update_question_endpoint(
    *, session: SessionDep, id: int, question_in: QuestionUpdate
) -> Any:
    return update_question_controller(session, id, question_in)


@router.delete("/{id}")
def delete_question_endpoint(session: SessionDep, id: int) -> Any:
    return delete_question_controller(session, id)
