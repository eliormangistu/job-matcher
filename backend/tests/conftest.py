import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import Base, get_db
from app.cache.redis import redis_client
from app.services.auth import verify_google_token

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from app.services.auth import verify_google_token


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    app.dependency_overrides[verify_google_token] = lambda: {"sub": "test-user"}
    yield TestClient(app)

    keys = list(redis_client.scan_iter(match="jobs:page:*"))
    if keys:
        redis_client.delete(*keys)

    app.dependency_overrides.clear()
