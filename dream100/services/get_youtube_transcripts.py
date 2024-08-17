import time
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from dream100.db_config import create_session
from dream100.models.content import ContentStatus
from dream100.models.web_property import WebPropertyType
from dream100.context.contents import ContentContext
import logging

logger = logging.getLogger(__name__)


class GetYoutubeTranscripts:
    def __init__(self, influencer_id=None, session=None, batch_size=None, delay=1):
        self.influencer_id = influencer_id
        if session:
            self.session = session
            self.should_close_session = False
        else:
            self.session, _ = create_session()
            self.should_close_session = True
        self.content_context = ContentContext(self.session)
        self.last_request_time = 0
        self.request_interval = delay
        self.batch_size = batch_size

    def get_youtube_video_id(self, url):
        parsed_url = urlparse(url)
        if parsed_url.hostname in ("youtu.be", "www.youtu.be"):
            return parsed_url.path[1:]
        if parsed_url.hostname in ("youtube.com", "www.youtube.com"):
            if parsed_url.path == "/watch":
                return parse_qs(parsed_url.query)["v"][0]
            if parsed_url.path.startswith(("/embed/", "/v/")):
                return parsed_url.path.split("/")[2]
        return None

    def get_youtube_transcript(self, video_url):
        current_time = time.time()
        if current_time - self.last_request_time < self.request_interval:
            time.sleep(self.request_interval - (current_time - self.last_request_time))

        try:
            video_id = self.get_youtube_video_id(video_url)
            if not video_id:
                raise ValueError(f"Invalid YouTube URL: {video_url}")

            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            full_transcript = " ".join([entry["text"] for entry in transcript])

            self.last_request_time = time.time()
            return full_transcript
        except Exception as e:
            logger.info(f"Error fetching transcript for {video_url}: {str(e)}")
            return None

    def get_and_update_transcripts(self):
        contents = self.content_context.list_contents(
            web_property_type=WebPropertyType.YOUTUBE,
            content_statuses=[ContentStatus.NONE, ContentStatus.WARNING],
            batch_size=self.batch_size,
            influencer_id=self.influencer_id,
        )

        for content in contents:
            logger.info(
                f"Processing YouTube content ID: {content.id}, URL: {content.link}"
            )
            transcript = self.get_youtube_transcript(content.link)

            if transcript:
                try:
                    updated_content = self.content_context.update_content(
                        content.id, scraped_content=transcript, status=ContentStatus.OK
                    )
                    if updated_content:
                        logger.info(
                            f"Updated transcript for YouTube content ID: {content.id}"
                        )
                    else:
                        logger.info(
                            f"Failed to update YouTube content ID: {content.id}"
                        )
                except Exception as e:
                    logger.info(
                        f"Error updating YouTube content ID: {content.id}: {str(e)}"
                    )
                    self.content_context.update_content(
                        content.id, status=ContentStatus.ERROR
                    )
            else:
                logger.info(
                    f"Failed to fetch transcript for YouTube content ID: {content.id}"
                )
                self.content_context.update_content(
                    content.id, status=ContentStatus.ERROR
                )

        if self.should_close_session:
            self.session.close()
        logger.info("YouTube transcript retrieval and update process completed.")


def get_youtube_transcripts(influencer_id=None, session=None, batch_size=None, delay=1):
    service = GetYoutubeTranscripts(influencer_id, session, batch_size, delay)
    service.get_and_update_transcripts()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Get YouTube Transcripts")
    parser.add_argument(
        "--batch_size", type=int, default=None, help="Batch size for processing"
    )
    parser.add_argument("--delay", type=int, default=1, help="Delay between requests")
    parser.add_argument(
        "--influencer_id",
        type=int,
        default=None,
        help="Influencer ID to filter contents",
    )

    args = parser.parse_args()
    get_youtube_transcripts(
        batch_size=args.batch_size, delay=args.delay, influencer_id=args.influencer_id
    )
