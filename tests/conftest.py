import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.config import setting
from app.db import Base, get_db
from app.main import app

engine = create_engine(setting.test_database_url)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def db():
    """A fresh, empty database for each test."""
    Base.metadata.create_all(engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)

@pytest.fixture
def client(db):
    """An HTTP client whose routes use the test database.""" 
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()