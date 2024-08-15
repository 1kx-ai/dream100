import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dream100_api.main import app
from dream100.db_config import Base, get_db
from dream100.models.project import Project
from dream100_api.auth.dependencies import get_current_user

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def override_get_current_user():
    return {"username": "testuser"}

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_project(test_db):
    response = client.post("/projects", json={"name": "Test Project", "description": "Test Description"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Project"
    assert response.json()["description"] == "Test Description"

def test_list_projects(test_db):
    response = client.get("/projects")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_project(test_db):
    response = client.post("/projects", json={"name": "Test Project", "description": "Test Description"})
    project_id = response.json()["id"]
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Project"
    assert response.json()["description"] == "Test Description"

def test_update_project(test_db):
    response = client.post("/projects", json={"name": "Test Project", "description": "Test Description"})
    project_id = response.json()["id"]
    response = client.put(f"/projects/{project_id}", json={"name": "Updated Project", "description": "Updated Description"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Project"
    assert response.json()["description"] == "Updated Description"

def test_delete_project(test_db):
    response = client.post("/projects", json={"name": "Test Project", "description": "Test Description"})
    project_id = response.json()["id"]
    response = client.delete(f"/projects/{project_id}")
    assert response.status_code == 204
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 404
