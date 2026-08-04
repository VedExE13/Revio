import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import get_db
from app.core.config import settings

test_engine = create_engine(
    settings.test_database_url,
    echo = False,
)

TestSessionLocal = sessionmaker(
    autocommit = False,
    autoflush= False,
    bind = test_engine,

)

def override_get_db():
    db = TestSessionLocal()
    try: 
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    yield client

    del app.dependency_overrides[get_db]