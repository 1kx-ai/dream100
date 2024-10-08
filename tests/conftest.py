import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dream100.db_config import Base, get_db, init_db
from dream100_api.main import app
from fastapi.testclient import TestClient
from config import config
from dream100.models.project import Project
from dream100.models.influencer import Influencer
from dream100.models.web_property import WebProperty, WebPropertyType
from dream100.models.content import Content, ContentStatus
from dream100.models.content_embedding import ContentEmbedding
from dream100.utilities import model as original_model
from tests.mocks.mock_model import MockEmbeddingModel
from tests.test_helpers import create_float_array


@pytest.fixture(scope="function", autouse=True)
def mock_embedding_model():
    original_instance = original_model.EmbeddingModel._instance
    original_model.EmbeddingModel._instance = MockEmbeddingModel()
    yield
    original_model.EmbeddingModel._instance = original_instance


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
    def _create_influencer(name="Test Influencer", project=None):
        influencer = Influencer(name=name)
        if project:
            influencer.projects.append(project)
        db_session.add(influencer)
        db_session.commit()
        db_session.refresh(influencer)
        return influencer

    return _create_influencer


@pytest.fixture(scope="function")
def create_web_property(db_session, create_influencer):
    def _create_web_property(
        influencer_id=None,
        type="youtube",
        url="https://www.youtube.com/testchannel",
        followers=1000,
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


@pytest.fixture(scope="function")
def create_content(db_session, create_web_property):
    def _create_content(
        web_property_id=None,
        link="https://www.example.com",
        scraped_content=None,
        views=0,
        status=ContentStatus.NONE,
    ):
        if not web_property_id:
            web_property = create_web_property()
            web_property_id = web_property.id
        content = Content(
            web_property_id=web_property_id,
            link=link,
            scraped_content=scraped_content,
            views=views,
            status=status,
        )
        db_session.add(content)
        db_session.commit()
        db_session.refresh(content)
        return content

    return _create_content


@pytest.fixture(scope="function")
def create_content_embedding(db_session, create_content):
    def _create_content_embedding(
        content_id=None, chunk_text="Test chunk text", embedding=None
    ):
        if not content_id:
            content = create_content()
            content_id = content.id
        if embedding is None:
            embedding = create_float_array(384)
        content_embedding = ContentEmbedding(
            content_id=content_id, chunk_text=chunk_text, embedding=embedding
        )
        db_session.add(content_embedding)
        db_session.commit()
        db_session.refresh(content_embedding)
        return content_embedding

    return _create_content_embedding
