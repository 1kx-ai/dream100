import pytest
from fastapi.testclient import TestClient
from dream100_api.main import app
from dream100.models.content_embedding import ContentEmbedding
from test_helpers import create_float_array


def test_list_content_embeddings(client, auth_headers, create_content, create_content_embedding):
    content = create_content()
    for i in range(3):
        create_content_embedding(content.id, f"Chunk {i}", create_float_array(384, i))

    response = client.get("/content_embeddings/list", headers=auth_headers)
    assert response.status_code == 200
    embeddings = response.json()
    assert len(embeddings) == 3
    assert all(isinstance(embedding, dict) for embedding in embeddings)
    assert all("id" in embedding for embedding in embeddings)
    assert all("content_id" in embedding for embedding in embeddings)
    assert all("chunk_text" in embedding for embedding in embeddings)
    assert all("embedding" in embedding for embedding in embeddings)


def test_list_content_embeddings_empty(client, auth_headers):
    response = client.get("/content_embeddings/list", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "No content embeddings found"


def test_list_content_embeddings_with_pagination(client, auth_headers, create_content, create_content_embedding):
    content = create_content()
    for i in range(15):
        create_content_embedding(content.id, f"Chunk {i}", create_float_array(384, i))

    # Test first page
    response = client.get("/content_embeddings/list?offset=0&limit=10", headers=auth_headers)
    assert response.status_code == 200
    embeddings = response.json()
    assert len(embeddings) == 10

    # Test second page
    response = client.get("/content_embeddings/list?offset=10&limit=10", headers=auth_headers)
    assert response.status_code == 200
    embeddings = response.json()
    assert len(embeddings) == 5


def test_list_content_embeddings_with_search(client, auth_headers, create_content, create_content_embedding):
    content = create_content()
    create_content_embedding(content.id, "Apple banana", create_float_array(384))
    create_content_embedding(content.id, "Cherry date", create_float_array(384))
    create_content_embedding(content.id, "Elderberry fig", create_float_array(384))

    response = client.get("/content_embeddings/list?search=banana", headers=auth_headers)
    assert response.status_code == 200
    embeddings = response.json()
    assert len(embeddings) == 1
    assert embeddings[0]["chunk_text"] == "Apple banana"

    response = client.get("/content_embeddings/list?search=berry", headers=auth_headers)
    assert response.status_code == 200
    embeddings = response.json()
    assert len(embeddings) == 1
    assert embeddings[0]["chunk_text"] == "Elderberry fig"

    response = client.get("/content_embeddings/list?search=grape", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "No content embeddings found"
