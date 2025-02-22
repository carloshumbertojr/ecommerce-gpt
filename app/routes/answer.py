from typing import Any
from fastapi import APIRouter

from app.config.deps import SessionDep
from app.models.answer import AnswerCreate, AnswerPublic, AnswerUpdate
from app.controllers.answer import (
    create_answer_controller,
    delete_answer_controller,
    read_answer_controller,
    update_answer_controller,
)

router = APIRouter()


@router.post("/", response_model=AnswerPublic)
def create_answer_endpoint(
    *,
    session: SessionDep,
    answer_in: AnswerCreate,
) -> Any:
    return create_answer_controller(session, answer_in)


@router.get("/{id}", response_model=AnswerPublic)
def read_answer_endpoint(session: SessionDep, id: int) -> Any:
    return read_answer_controller(session, id)


@router.put("/{id}", response_model=AnswerPublic)
def update_answer_endpoint(
    *, session: SessionDep, id: int, answer_in: AnswerUpdate
) -> Any:
    return update_answer_controller(session, id, answer_in)


@router.delete("/{id}")
def delete_answer_endpoint(session: SessionDep, id: int) -> Any:
    return delete_answer_controller(session, id)
