import pytest
from sqlalchemy.exc import SQLAlchemyError
from dream100.content_embeddings.content_embeddings import ContentEmbeddingContext
from dream100.models.content_embedding import ContentEmbedding
from test_helpers import create_float_array
import numpy as np


@pytest.fixture
def content_embedding_context(db_session):
    return ContentEmbeddingContext(db_session)


def test_create_embedding(content_embedding_context, db_session):
    content_id = 1
    chunk_text = "Sample text"
    embedding = create_float_array(384)
    content_embedding = content_embedding_context.create_embedding(
        content_id, chunk_text, embedding
    )
    assert content_embedding.id is not None
    assert content_embedding.content_id == content_id
    assert content_embedding.chunk_text == chunk_text
    assert np.allclose(np.array(content_embedding.embedding), np.array(embedding))


def test_get_embedding(content_embedding_context, db_session):
    content_id = 1
    chunk_text = "Sample text"
    embedding = create_float_array(384)
    content_embedding = content_embedding_context.create_embedding(
        content_id, chunk_text, embedding
    )
    fetched_embedding = content_embedding_context.get_embedding(content_embedding.id)
    assert fetched_embedding == content_embedding


def test_delete_embedding(content_embedding_context, db_session):
    content_id = 1
    chunk_text = "Sample text"
    embedding = create_float_array(384)
    content_embedding = content_embedding_context.create_embedding(
        content_id, chunk_text, embedding
    )
    result = content_embedding_context.delete_embedding(content_embedding.id)
    assert result is True
    assert content_embedding_context.get_embedding(content_embedding.id) is None


def test_update_embedding(content_embedding_context, db_session):
    content_id = 1
    chunk_text = "Sample text"
    embedding = create_float_array(384)
    content_embedding = content_embedding_context.create_embedding(
        content_id, chunk_text, embedding
    )
    new_chunk_text = "Updated text"
    new_embedding = create_float_array(384, 1)
    updated_embedding = content_embedding_context.update_embedding(
        content_embedding.id, new_chunk_text, new_embedding
    )
    assert updated_embedding.chunk_text == new_chunk_text
    assert np.allclose(np.array(updated_embedding.embedding), np.array(new_embedding))


def test_list_embeddings(content_embedding_context, db_session):
    content_id = 1
    chunk_text = "Sample text"
    embedding = create_float_array(384)
    content_embedding_context.create_embedding(content_id, chunk_text, embedding)
    embeddings = content_embedding_context.list_embeddings(content_id=content_id)
    assert len(embeddings) == 1
    assert embeddings[0].chunk_text == chunk_text


def test_get_embedding_count(content_embedding_context, db_session):
    content_id = 1
    chunk_text = "Sample text"
    embedding = create_float_array(384)
    content_embedding_context.create_embedding(content_id, chunk_text, embedding)
    count = content_embedding_context.get_embedding_count(content_id=content_id)
    assert count == 1
