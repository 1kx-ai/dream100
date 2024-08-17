import pytest
from unittest.mock import patch
from dream100.services.embed_youtube_transcripts import embed_youtube_transcripts
from dream100.context.content_embeddings import ContentEmbeddingContext
from tests.mocks.mock_model import MockEmbeddingModel


def test_embed_youtube_transcripts(db_session, create_content):
    with patch("dream100.content_embeddings.model.EmbeddingModel", MockEmbeddingModel):
        content = create_content(scraped_content="Scraped Content")
        content_id = content.id
        embed_youtube_transcripts(session=db_session)
        embedding_context = ContentEmbeddingContext(db_session)
        embeddings = embedding_context.get_embeddings_for_content(content_id)

        assert len(embeddings) > 0
        for embedding in embeddings:
            assert len(embedding.embedding) == 384
