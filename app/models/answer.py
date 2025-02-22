from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT


# Shared properties
class AnswerBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(sa_column=Column(TEXT))
    endpoint: str
    ml_product_id: str
    option_type: str


class Answer(AnswerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)


# Properties to receive on Answer creation
class AnswerCreate(AnswerBase):
    title: str = Field(min_length=1, max_length=255)


# Properties to receive on Answer update
class AnswerUpdate(AnswerBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Properties to return via API, id is always required
class AnswerPublic(AnswerBase):
    id: int


class AnswersPublic(SQLModel):
    data: list[AnswerPublic]
    count: int
