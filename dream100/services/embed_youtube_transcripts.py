from dream100.db_config import create_session
from dream100.models.content import Content, ContentStatus
from dream100.models.web_property import WebProperty, WebPropertyType
from dream100.context.contents import ContentContext
from dream100.context.content_embeddings import ContentEmbeddingContext
from dream100.utilities.embedding_utils import (
    chunk_content,
    batch_create_embeddings,
)
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbedYoutubeTranscripts:
    def __init__(self, batch_size=100, session=None, influencer_id=None):
        self.influencer_id = influencer_id
        if session:
            self.session = session
            self.should_close_session = False
        else:
            self.session, _ = create_session()
            self.should_close_session = True
        self.content_context = ContentContext(self.session)
        self.embedding_context = ContentEmbeddingContext(self.session)
        self.batch_size = batch_size

    def process_transcripts(self):
        content_iterator = self.content_context.iter_contents(
            batch_size=100,
            web_property_type=WebPropertyType.YOUTUBE,
            content_statuses=[ContentStatus.NONE],
            has_scraped_content=True,
            influencer_id=self.influencer_id,
        )

        for content in content_iterator:
            self.process_content(content)

    def process_content(self, content):
        try:
            logger.info(f"Processing content ID: {content.id}")

            chunks = chunk_content(content.scraped_content)
            embeddings = batch_create_embeddings(chunks)

            for chunk, embedding in zip(chunks, embeddings):
                self.embedding_context.create_embedding(content.id, chunk, embedding)

            # Use update_content instead of update_content_status
            self.content_context.update_content(content.id, status=ContentStatus.OK)

            logger.info(
                f"Processed YouTube content ID: {content.id}, URL: {content.link}"
            )

        except Exception as e:
            logger.error(f"Error processing YouTube content ID: {content.id}: {str(e)}")
            logger.exception("Full traceback:")


def embed_youtube_transcripts(batch_size=100, session=None, influencer_id=None):
    service = EmbedYoutubeTranscripts(batch_size, session, influencer_id)
    service.process_transcripts()


if __name__ == "__main__":
    embed_youtube_transcripts()
