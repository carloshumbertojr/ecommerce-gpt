from datetime import datetime
from fastapi import Response
from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT


# Shared properties
class QuestionBase(SQLModel):
    ml_product_id: str
    question: str = Field(sa_column=Column(TEXT))
    description: str = Field(sa_column=Column(TEXT))
    human_answer: str = Field(sa_column=Column(TEXT))
    ai_answer: str | None = Field(default=None)
    model: str | None = Field(default=None)
    similarity: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    execution_time: str | None = Field(default=None)


class Question(QuestionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question: str = Field(sa_column=Column(TEXT))


# Properties to receive on Question creation
class QuestionCreate(QuestionBase):
    question: str = Field(sa_column=Column(TEXT))


# Properties to receive on Question update
class QuestionUpdate(QuestionBase):
    question: str | None = Field(default=None, sa_column=Column(TEXT))  # type: ignore


# Properties to return via API, id is always required
class QuestionPublic(QuestionBase):
    id: int


class QuestionsPublic(SQLModel):
    data: list[QuestionPublic]
    count: int


class QuestionResponse(Response):
    ai_answer: str
    execution_time: str
