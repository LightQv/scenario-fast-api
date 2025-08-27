from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.settings import settings

# Configuration SQLAlchemy
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_database_session() -> Generator[Session, None, None]:
    """
    Dépendance FastAPI pour obtenir une session de base de données.
    Utilise le pattern de générateur pour s'assurer que la session est fermée.
    """
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()