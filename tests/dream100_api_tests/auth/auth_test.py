import os
import pytest
import logging
from fastapi.testclient import TestClient
from dream100_api.main import app
from dream100_api.auth.bearer_auth import BearerAuth
from dream100_api.auth.middleware import AuthMiddleware
from dotenv import load_dotenv
from config import config


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load test environment variables
load_dotenv(".env.test")

def get_test_client():
    auth_provider = BearerAuth()
    app.add_middleware(AuthMiddleware, auth_provider=auth_provider)
    return TestClient(app)

@pytest.fixture(scope="module")
def client():
    return get_test_client()

def test_projects_route_with_valid_token(client):
    test_api_key = config.TEST_API_KEY
    assert test_api_key, "TEST_API_KEY not set in .env file"
    logger.debug(f"Using TEST_API_KEY: {test_api_key}")
    headers = {"Authorization": f"Bearer {test_api_key}"}
    response = client.get("/projects", headers=headers)
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response body: {response.text}")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, body: {response.text}"
    assert "projects" in response.json()

def test_projects_route_with_invalid_token(client):
    headers = {"Authorization": "Bearer invalid-token"}
    response = client.get("/projects", headers=headers)
    assert response.status_code == 401, f"Unexpected status code: {response.status_code}, body: {response.text}"

def test_projects_route_without_token(client):
    response = client.get("/projects")
    assert response.status_code == 401, f"Unexpected status code: {response.status_code}, body: {response.text}"