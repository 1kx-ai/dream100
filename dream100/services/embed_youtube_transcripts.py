from dream100.db_config import create_session
from dream100.models.content import Content, ContentStatus
from dream100.models.web_property import WebProperty, WebPropertyType
from dream100.context.contents import ContentContext
from dream100.context.content_embeddings import ContentEmbeddingContext
from dream100.utilities.embedding_utils import (
    chunk_content,
    batch_create_embeddings,
)
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbedYoutubeTranscripts:
    def __init__(self, batch_size=100, session=None):
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
        try:
            # Query for YouTube content with OK status and scraped_content
            stmt = (
                select(Content)
                .join(Content.web_property)
                .filter(
                    WebProperty.type == WebPropertyType.YOUTUBE,
                    Content.status == ContentStatus.OK,
                    Content.scraped_content.isnot(None),
                )
                .options(joinedload(Content.web_property))
            )

            total_count = self.session.scalar(
                select(func.count()).select_from(stmt.subquery())
            )
            logger.info(f"Found {total_count} YouTube transcripts to process")

            for i in range(0, total_count, self.batch_size):
                batch = self.session.scalars(
                    stmt.offset(i).limit(self.batch_size)
                ).all()
                self.process_batch(batch)
                logger.info(f"Processed batch {i // self.batch_size + 1}")

            logger.info("Finished processing all YouTube transcripts")

        except Exception as e:
            logger.error(f"An error occurred while processing transcripts: {str(e)}")
        finally:
            if self.should_close_session:
                self.session.close()

    def process_batch(self, contents):
        for content in contents:
            try:
                # Double-check that this content is indeed from YouTube
                if content.web_property.type != WebPropertyType.YOUTUBE:
                    logger.warning(f"Skipping non-YouTube content ID: {content.id}")
                    continue

                chunks = chunk_content(content.scraped_content)
                embeddings = batch_create_embeddings(chunks)

                for chunk, embedding in zip(chunks, embeddings):
                    self.embedding_context.create_embedding(
                        content.id, chunk, embedding
                    )

                logger.info(
                    f"Processed YouTube content ID: {content.id}, URL: {content.link}"
                )

            except Exception as e:
                logger.error(
                    f"Error processing YouTube content ID: {content.id}: {str(e)}"
                )
                self.session.rollback()
                continue


def embed_youtube_transcripts(batch_size=100, session=None):
    service = EmbedYoutubeTranscripts(batch_size, session)
    service.process_transcripts()


if __name__ == "__main__":
    embed_youtube_transcripts()
