from sqlalchemy import create_engine, text
from sqlalchemy import StaticPool
from sqlalchemy.orm import sessionmaker
from database import Base
from fastapi.testclient import TestClient
import pytest
from main import app  
from models import Todos
from models import Users
from utils.hash import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"\

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "lukas", 'id': 1, "user_role": "admin"}

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code",
        description="Need to learn",
        priority=5,
        complete=False,
        owner_id=1
    )
    db = TestingSessionLocal()

    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    user = Users(
        id=1,
        username="lukas",
        email="lukas@example.com",
        first_name="Lukas",
        last_name="Example",
        role="admin",
        phone_number="1234567890",
        hashed_password=bcrypt_context.hash("test")
    )
    db.add(user)
    db.commit()
    yield user
    db.delete(user)
    db.commit()
    db.close()