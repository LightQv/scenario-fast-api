import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_database_session, Base
from app.models import User
from app.core.security import hash_password

# Base de données en mémoire pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_database():
    try:
        database_session = TestingSessionLocal()
        yield database_session
    finally:
        database_session.close()


@pytest.fixture
def database_session():
    Base.metadata.create_all(bind=engine)
    database_session = TestingSessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(database_session):
    app.dependency_overrides[get_database_session] = override_get_database
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_user(database_session):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("testpassword123")
    )
    database_session.add(user)
    database_session.commit()
    database_session.refresh(user)
    return user