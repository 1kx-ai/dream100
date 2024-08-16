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
