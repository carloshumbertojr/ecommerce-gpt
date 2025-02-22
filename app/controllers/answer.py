from typing import Any

from app.config.deps import SessionDep
from app.models.answer import Answer, AnswerCreate, AnswerUpdate
from app.services.answer import (
    create_answer_service,
    delete_answer_service,
    read_answer_service,
    update_answer_service,
)


def create_answer_controller(
    session: SessionDep,
    answer_in: AnswerCreate,
) -> Any:
    """
    Handle create answer request.
    """
    answer = Answer.model_validate(answer_in)
    answer = create_answer_service(session, answer)
    return answer


def read_answer_controller(session: SessionDep, id: int) -> Any:
    return read_answer_service(session, id)


def update_answer_controller(
    session: SessionDep, id: int, answer_in: AnswerUpdate
) -> Any:
    return update_answer_service(session, id, answer_in)


def delete_answer_controller(session: SessionDep, id: int) -> Any:
    return delete_answer_service(session, id)
