import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dream100.db_config import Base, get_db, init_db
from dream100_api.main import app
from fastapi.testclient import TestClient
from config import config
from dream100.models.project import Project
from dream100.models.influencer import Influencer


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


@pytest.fixture(scope="function")
def create_project(db_session):
    def _create_project(name="Test Project", description="Test Description"):
        project = Project(name=name, description=description)
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)
        return project

    return _create_project


@pytest.fixture(scope="function")
def create_projects(create_project):
    def _create_projects(count=2):
        return [
            create_project(f"Project {i}", f"Description {i}")
            for i in range(1, count + 1)
        ]

    return _create_projects
@pytest.fixture(scope="function")
def create_influencer(db_session):

@pytest.fixture(scope="function")
def create_web_property(db_session, create_influencer):
    def _create_web_property(
        influencer_id=None, type="YOUTUBE", url="https://www.youtube.com/testchannel", followers=None
    ):
        if not influencer_id:
            influencer = create_influencer()
            influencer_id = influencer.id
        web_property = WebProperty(
            influencer_id=influencer_id,
            type=WebPropertyType(type),
            url=url,
            followers=followers,
        )
        db_session.add(web_property)
        db_session.commit()
        db_session.refresh(web_property)
        return web_property

    return _create_web_property
    def _create_influencer(name="Test Influencer"):
        influencer = Influencer(name=name)
        db_session.add(influencer)
        db_session.commit()
        db_session.refresh(influencer)
        return influencer

    return _create_influencer
