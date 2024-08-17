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


def test_embed_youtube_transcripts_with_influencer_id(
    db_session, create_content, create_influencer, create_web_property
):
    with patch("dream100.content_embeddings.model.EmbeddingModel", MockEmbeddingModel):
        influencer = create_influencer(name="Test Influencer")
        web_property = create_web_property(
            influencer_id=influencer.id,
            type="youtube",
            url="https://www.youtube.com/testchannel",
        )
        content = create_content(
            web_property_id=web_property.id, scraped_content="Scraped Content"
        )
        content_id = content.id
        embed_youtube_transcripts(session=db_session, influencer_id=influencer.id)
        embedding_context = ContentEmbeddingContext(db_session)
        embeddings = embedding_context.get_embeddings_for_content(content_id)

        assert len(embeddings) > 0
        for embedding in embeddings:
            assert len(embedding.embedding) == 384
