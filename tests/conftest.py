import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Agent, Customer

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

@pytest.fixture
def agent(db):
    """One agent savd in the test database."""
    a = Agent(name="Test Agent", email="agent@test.com",
              phone_number="+359880000000", password_hash="TEMP")
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

@pytest.fixture
def customer(db):
    """One customer saved in the test database."""
    c = Customer(name="Test Customer", email="customer@test.com",
              company="Lai corp.", password_hash="TEMP")
    db.add(c)
    db.commit()
    db.refresh(c)
    return c