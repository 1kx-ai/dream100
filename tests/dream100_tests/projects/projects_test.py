import pytest
from dream100.projects.projects import ProjectContext
from tests.test_helpers import db_engine, db_session  # Import the fixtures

@pytest.fixture
def project_context(db_session):
    return ProjectContext(db_session)

def test_create_project(project_context):
    project = project_context.create_project("Test Project", "This is a test project")
    assert project.name == "Test Project"
    assert project.description == "This is a test project"

def test_get_project(project_context):
    project = project_context.create_project("Another Project", "Another test project")
    retrieved_project = project_context.get_project(project.id)
    assert retrieved_project.name == "Another Project"
    assert retrieved_project.description == "Another test project"

def test_update_project(project_context):
    project = project_context.create_project("Update Me", "Original description")
    updated_project = project_context.update_project(project.id, name="Updated Project", description="New description")
    assert updated_project.name == "Updated Project"
    assert updated_project.description == "New description"

def test_delete_project(project_context):
    project = project_context.create_project("Delete Me", "To be deleted")
    assert project_context.delete_project(project.id) == True
    assert project_context.get_project(project.id) is None

def test_list_projects(project_context):
    project_context.create_project("Project 1", "Description 1")
    project_context.create_project("Project 2", "Description 2")
    projects = project_context.list_projects()
    assert len(projects) >= 2
    assert any(p.name == "Project 1" for p in projects)
    assert any(p.name == "Project 2" for p in projects)