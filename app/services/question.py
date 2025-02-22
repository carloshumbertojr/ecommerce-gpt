from datetime import datetime
from typing import Any
from fastapi import HTTPException
from strsimpy.normalized_levenshtein import NormalizedLevenshtein

from app.config.config import settings

from app.classes.chat import GPTChat
from app.config.deps import SessionDep
from app.models.question import Question, QuestionResponse, QuestionUpdate


def create_question_service(
    session: SessionDep,
    question: Question,
) -> QuestionResponse:
    """
    Processar e criar uma entrada de pergunta.

    Esta função processa uma pergunta usando um chatbot para gerar uma resposta de IA,
    calcula o tempo de execução, similaridade com uma resposta humana e armazena a
    entrada da pergunta no banco de dados.

    Parâmetros:
    session (SessionDep): A sessão do banco de dados.
    question (Question): A pergunta a ser processada.

    Retorna:
    QuestionResponse: A pergunta processada com resposta de IA e outros detalhes.
    """

    timestamp = datetime.now()

    chat = GPTChat()

    question.ai_answer = process_description(
        chat, question.question, question.description, settings.BASE_NAME_CHAT_MODEL
    )

    question.execution_time = str(datetime.now() - timestamp)

    levenshtein = NormalizedLevenshtein()

    # Verifica a similaridade entre a nova pergunta e a resposta humana
    question.similarity = levenshtein.similarity(
        question.ai_answer, question.human_answer
    )

    # Adicionar o modelo
    question.model = settings.BASE_NAME_CHAT_MODEL

    # Salva a resposta no banco de dados
    session.add(question)
    session.commit()
    session.refresh(question)

    return {"ai_answer": question.ai_answer}


def process_description(
    chat_bot: GPTChat, user_message: str, description: str, model_name: str
) -> str:
    """Process the item description and get a response from the chatbot."""
    return chat_bot.message_bot(user_message, description, model=model_name)


def read_question_service(session: SessionDep, id: int) -> Any:
    question = session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    return question


def update_question_service(
    session: SessionDep, id: int, question_in: QuestionUpdate
) -> Any:
    question = session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")

    update_dict = question_in.model_dump(exclude_unset=True)
    question.sqlmodel_update(update_dict)
    session.add(question)
    session.commit()
    session.refresh(question)
    return question


def delete_question_service(session: SessionDep, id: int) -> Any:
    question = session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")

    session.delete(question)
    session.commit()
    return {"message": "Answer deleted successfully"}
