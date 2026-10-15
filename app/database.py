from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings


def normalize_database_url(url: str) -> str:
    """Ensure cloud PostgreSQL URLs use the psycopg 3 driver installed here."""
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url.removeprefix("postgres://")
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url.removeprefix("postgresql://")
    return url


class Base(DeclarativeBase):
    pass


engine = create_engine(normalize_database_url(settings.DATABASE_URL))

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
