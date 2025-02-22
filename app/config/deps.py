from fastapi import Depends
from sqlmodel import Session
from typing import Annotated
from collections.abc import Generator

from app.config.db import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
