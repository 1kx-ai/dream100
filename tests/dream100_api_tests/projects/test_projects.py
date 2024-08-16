import pytest
from dream100.models.project import Project


def test_create_project(client, auth_headers):
    response = client.post(
        "/projects",
        json={"name": "Test Project", "description": "Test Description"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Project"
    assert response.json()["description"] == "Test Description"


def test_list_projects(client, auth_headers):
    response = client.post(
        "/projects",
        json={"name": "Test Project", "description": "Test Description"},
        headers=auth_headers,
    )
    response = client.get("/projects", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_project(client, auth_headers):
    response = client.post(
        "/projects",
        json={"name": "Test Project", "description": "Test Description"},
        headers=auth_headers,
    )
    project_id = response.json()["id"]
    response = client.get(f"/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Project"
    assert response.json()["description"] == "Test Description"


def test_update_project(client, auth_headers):
    response = client.post(
        "/projects",
        json={"name": "Test Project", "description": "Test Description"},
        headers=auth_headers,
    )
    project_id = response.json()["id"]
    response = client.put(
        f"/projects/{project_id}",
        json={"name": "Updated Project", "description": "Updated Description"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Project"
    assert response.json()["description"] == "Updated Description"


def test_delete_project(client, auth_headers):
    response = client.post(
        "/projects",
        json={"name": "Test Project", "description": "Test Description"},
        headers=auth_headers,
    )
    project_id = response.json()["id"]
    response = client.delete(f"/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 404
