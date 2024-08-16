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
            "type": "youtube",
            "url": "https://www.youtube.com/testchannel",
            "followers": 1000,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "youtube"
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


import pytest
from dream100.models.web_property import WebProperty, WebPropertyType


def test_create_web_property(client, auth_headers, create_influencer):
    influencer = create_influencer()
    response = client.post(
        "/web_properties",
        json={
            "influencer_id": influencer.id,
            "type": "youtube",
            "url": "https://www.youtube.com/testchannel",
            "followers": 1000,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["type"] == "youtube"
    assert response.json()["url"] == "https://www.youtube.com/testchannel"
    assert response.json()["followers"] == 1000


def test_get_web_property(client, auth_headers, create_web_property):
    web_property = create_web_property()
    response = client.get(f"/web_properties/{web_property.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["type"] == "youtube"
    assert response.json()["url"] == "https://www.youtube.com/testchannel"
    assert response.json()["followers"] == 1000


def test_update_web_property(client, auth_headers, create_web_property):
    web_property = create_web_property()
    response = client.put(
        f"/web_properties/{web_property.id}",
        json={
            "type": "twitter",
            "url": "https://www.twitter.com/updatedchannel",
            "followers": 2000,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["type"] == "twitter"
    assert response.json()["url"] == "https://www.twitter.com/updatedchannel"
    assert response.json()["followers"] == 2000


def test_delete_web_property(client, auth_headers, create_web_property):
    web_property = create_web_property()
    response = client.delete(f"/web_properties/{web_property.id}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/web_properties/{web_property.id}", headers=auth_headers)
    assert response.status_code == 404


def test_list_web_properties(client, auth_headers, create_web_property):
    web_property = create_web_property()
    response = client.get("/web_properties", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
