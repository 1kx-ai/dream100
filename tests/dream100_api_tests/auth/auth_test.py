import pytest
import logging
from config import config
from config import config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_projects_route_with_valid_token(client, auth_headers):
    logger.debug(f"Using auth headers: {auth_headers}")
    response = client.post(
        "/projects",
        headers=auth_headers,
        json={"name": "Project 1", "description": "Description 1"},
    )
    response = client.get("/projects", headers=auth_headers)
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response body: {response.text}")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, body: {response.text}"
    assert response.json() == [
        {"description": "Description 1", "id": 1, "name": "Project 1"}
    ]


def test_projects_route_with_invalid_token(client):
    headers = {"Authorization": "Bearer invalid-token"}
    response = client.get("/projects", headers=headers)
    assert response.status_code == 401, f"Unexpected status code: {response.status_code}, body: {response.text}"


def test_projects_route_without_token(client):
    response = client.get("/projects")
    assert response.status_code == 401, f"Unexpected status code: {response.status_code}, body: {response.text}"
