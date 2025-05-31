import os
from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends


DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    echo=False,          
    connect_args=connect_args,
)

def init_db() -> None:
    """
    Инициализирует базу данных, создавая все таблицы,
    описанные в metadata всех моделей SQLModel.
    """
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency для FastAPI: даёт в каждый роут постоянную сессию к БД
    и автоматически закрывает её после запроса.
    """
    with Session(engine) as session:
        yield session