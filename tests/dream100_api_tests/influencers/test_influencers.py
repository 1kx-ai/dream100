import pytest


def test_create_influencer(client, auth_headers, create_projects):
    projects = create_projects(2)
    project_ids = [project.id for project in projects]
    response = client.post(
        "/influencers",
        json={"name": "Test Influencer", "project_ids": project_ids},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Influencer"
    assert response.json()["project_ids"] == project_ids


def test_list_influencers(client, auth_headers, create_projects):
    projects = create_projects(2)
    project_ids = [project.id for project in projects]
    client.post(
        "/influencers",
        json={"name": "Test Influencer", "project_ids": project_ids},
        headers=auth_headers,
    )
    response = client.get("/influencers", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_influencer(client, auth_headers, create_projects):
    projects = create_projects(2)
    project_ids = [project.id for project in projects]
    create_response = client.post(
        "/influencers",
        json={"name": "Test Influencer", "project_ids": project_ids},
        headers=auth_headers,
    )
    influencer_id = create_response.json()["id"]
    response = client.get(f"/influencers/{influencer_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Influencer"
    assert response.json()["project_ids"] == project_ids


def test_update_influencer(client, auth_headers, create_projects):
    projects = create_projects(2)
    project_ids = [project.id for project in projects]
    create_response = client.post(
        "/influencers",
        json={"name": "Test Influencer", "project_ids": [project_ids[0]]},
        headers=auth_headers,
    )
    influencer_id = create_response.json()["id"]
    response = client.put(
        f"/influencers/{influencer_id}",
        json={"name": "Updated Influencer", "project_ids": [project_ids[1]]},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Influencer"
    assert response.json()["project_ids"] == [project_ids[1]]


def test_delete_influencer(client, auth_headers, create_projects):
    projects = create_projects(2)
    project_ids = [project.id for project in projects]
    create_response = client.post(
        "/influencers",
        json={"name": "Test Influencer", "project_ids": project_ids},
        headers=auth_headers,
    )
    influencer_id = create_response.json()["id"]
    response = client.delete(f"/influencers/{influencer_id}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/influencers/{influencer_id}", headers=auth_headers)
    assert response.status_code == 404
