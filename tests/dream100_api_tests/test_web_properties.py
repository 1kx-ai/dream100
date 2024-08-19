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
    # Create multiple web properties
    for _ in range(15):
        create_web_property()

    # Test default pagination (page 1, per_page 10)
    response = client.get("/web_properties", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["total"] == 15
    assert data["page"] == 1
    assert data["per_page"] == 10
    assert data["pages"] == 2

    # Test custom pagination
    response = client.get("/web_properties?page=2&per_page=5", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 5
    assert data["total"] == 15
    assert data["page"] == 2
    assert data["per_page"] == 5
    assert data["pages"] == 3

def test_list_web_properties_by_project(client, auth_headers, create_project, create_influencer, create_web_property):
    # Create projects
    project1 = create_project("Project 1")
    project2 = create_project("Project 2")

    # Create influencers and associate them with projects
    influencer1 = create_influencer("Influencer 1", project=project1)
    influencer2 = create_influencer("Influencer 2", project=project2)
    influencer3 = create_influencer("Influencer 3", project=project1)
    
    # Create web properties
    web_property1 = create_web_property(influencer_id=influencer1.id, type="youtube", url="https://www.youtube.com/channel1")
    web_property2 = create_web_property(influencer_id=influencer2.id, type="twitter", url="https://www.twitter.com/user2")
    web_property3 = create_web_property(influencer_id=influencer3.id, type="linkedin", url="https://www.linkedin.com/in/user3")
    
    # Test filtering by project_id
    response = client.get(f"/web_properties?project_id={project1.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert {wp['id'] for wp in data["items"]} == {web_property1.id, web_property3.id}
    assert data["total"] == 2
    
    # Test with non-existent project_id
    response = client.get("/web_properties?project_id=9999", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0
    assert data["total"] == 0

def test_list_web_properties_by_influencer(client, auth_headers, create_influencer, create_web_property):
    influencer = create_influencer("Test Influencer")
    for _ in range(5):
        create_web_property(influencer_id=influencer.id)

    response = client.get(f"/web_properties?influencer_id={influencer.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 5
    assert data["total"] == 5
    assert all(wp["influencer_id"] == influencer.id for wp in data["items"])
