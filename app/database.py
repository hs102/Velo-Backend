import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()


class Base(DeclarativeBase):
	pass


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
	DATABASE_URL,
	pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def db_ping() -> None:
	with engine.connect() as connection:
		connection.execute(text("SELECT 1"))
