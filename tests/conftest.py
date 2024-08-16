import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dream100.db_config import Base, get_db, init_db
from dream100_api.main import app
from fastapi.testclient import TestClient
from config import config


@pytest.fixture(scope="function")
def db_engine():
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    init_db(engine)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=db_engine
    )
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def auth_headers():
    API_KEY = config.API_KEY
    assert API_KEY, "API_KEY not set in .env file"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    return headers
