import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from dream100.models.web_property import WebProperty, WebPropertyType
from dream100_api.main import app


def test_create_web_property(client, db_session, auth_headers):
    response = client.post(
        "/web_properties",
        json={
            "influencer_id": 1,
            "type": "YOUTUBE",
            "url": "https://www.youtube.com/testchannel",
            "followers": 1000,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "YOUTUBE"
    assert data["url"] == "https://www.youtube.com/testchannel"
    assert data["followers"] == 1000


def test_get_web_property(client, create_web_property, auth_headers):
    web_property = create_web_property()
    response = client.get(f"/web_properties/{web_property.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == web_property.id
    assert data["url"] == web_property.url


def test_update_web_property(client, create_web_property, auth_headers):
    web_property = create_web_property()
    response = client.put(
        f"/web_properties/{web_property.id}",
        json={"url": "https://www.youtube.com/updatedchannel"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == "https://www.youtube.com/updatedchannel"


def test_delete_web_property(client, create_web_property, auth_headers):
    web_property = create_web_property()
    response = client.delete(f"/web_properties/{web_property.id}", headers=auth_headers)
    assert response.status_code == 204


def test_list_web_properties(client, create_web_property, auth_headers):
    create_web_property()
    create_web_property()
    response = client.get("/web_properties", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
