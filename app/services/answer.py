from typing import Any
from sqlalchemy import select
from fastapi import HTTPException
from strsimpy.normalized_levenshtein import NormalizedLevenshtein

from app.config.config import settings

from app.classes.chat import GPTChat
from app.config.deps import SessionDep
from app.models.answer import Answer, AnswerUpdate


def create_answer_service(
    session: SessionDep,
    answer: Answer,
) -> Any:
    """
    Processar resposta.

    Esta função processa a resposta verificando se já existe uma resposta
    para o mesmo produto e com um título similar. Se houver, ela retorna a
    resposta existente. Se não, ela gera uma resposta usando o chatbot e armazena
    a resposta no banco de dados.

    Parâmetros:
    session (SessionDep): A sessão do banco de dados.
    answer (Answer): A resposta a ser processada.

    Retorna:
    Any: A resposta processada.
    """

    levenshtein = NormalizedLevenshtein()

    # Recupera perguntas existentes para o mesmo produto
    stmt = select(Answer).where(Answer.ml_product_id == answer.ml_product_id).distinct()
    existing_answers = session.execute(stmt).scalars().all()

    # Verifica a similaridade entre a nova pergunta e as existentes
    for existing_answer in existing_answers:
        similarity = levenshtein.similarity(answer.title, existing_answer.title)
        if similarity >= settings.SIMILARITY_THRESHOLD:
            # Se a similaridade for maior que o limiar, retorna a pergunta existente
            return existing_answer

    # Caso contrario, gera uma resposta utilizando o chatbot
    chat = GPTChat()

    response_answer = process_description(
        chat, answer.title, answer.description, settings.BASE_NAME_CHAT_MODEL
    )

    answer.description = response_answer

    # Salva a resposta no banco de dados
    session.add(answer)
    session.commit()
    session.refresh(answer)

    return answer


def process_description(
    chat_bot: GPTChat, user_message: str, description: str, model_name: str
) -> str:
    """Process the item description and get a response from the chatbot."""
    return chat_bot.message_bot(user_message, description, model=model_name)


def read_answer_service(session: SessionDep, id: int) -> Any:
    answer = session.get(Answer, id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer


def update_answer_service(session: SessionDep, id: int, answer_in: AnswerUpdate) -> Any:
    answer = session.get(Answer, id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    update_dict = answer_in.model_dump(exclude_unset=True)
    answer.sqlmodel_update(update_dict)
    session.add(answer)
    session.commit()
    session.refresh(answer)
    return answer


def delete_answer_service(session: SessionDep, id: int) -> Any:
    answer = session.get(Answer, id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    session.delete(answer)
    session.commit()
    return {"message": "Answer deleted successfully"}
