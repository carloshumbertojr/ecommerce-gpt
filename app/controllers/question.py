from typing import Any

from app.config.deps import SessionDep
from app.models.question import Question, QuestionCreate, QuestionUpdate
from app.services.question import (
    create_question_service,
    delete_question_service,
    read_question_service,
    update_question_service,
)


def create_question_controller(
    session: SessionDep,
    question_in: QuestionCreate,
) -> Any:
    """
    Handle create question request.
    """
    question = Question.model_validate(question_in)
    question = create_question_service(session, question)
    return question


def read_question_controller(session: SessionDep, id: int) -> Any:
    return read_question_service(session, id)


def update_question_controller(
    session: SessionDep, id: int, question_in: QuestionUpdate
) -> Any:
    return update_question_service(session, id, question_in)


def delete_question_controller(session: SessionDep, id: int) -> Any:
    return delete_question_service(session, id)
