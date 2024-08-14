import time
from sqlalchemy import or_
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from dream100.db_config import create_session
from dream100.models.content import Content, ContentStatus
from dream100.models.web_property import WebProperty, WebPropertyType
from dream100.contents.contents import ContentContext


class GetYoutubeTranscripts:
    def __init__(self, batch_size=None, delay=1):
        self.session, _ = create_session()
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
            print(f"Error fetching transcript for {video_url}: {str(e)}")
            return None

    def get_and_update_transcripts(self):
        query = (
            self.session.query(Content)
            .join(Content.web_property)
            .filter(
                WebProperty.type == WebPropertyType.YOUTUBE,
                or_(
                    Content.status == ContentStatus.NONE,
                    Content.status == ContentStatus.WARNING,
                ),
            )
        )

        if self.batch_size:
            query = query.limit(self.batch_size)

        contents = query.all()

        for content in contents:
            print(f"Processing YouTube content ID: {content.id}, URL: {content.link}")
            transcript = self.get_youtube_transcript(content.link)

            if transcript:
                try:
                    updated_content = self.content_context.update_content(
                        content.id, scraped_content=transcript, status=ContentStatus.OK
                    )
                    if updated_content:
                        print(
                            f"Updated transcript for YouTube content ID: {content.id}"
                        )
                    else:
                        print(f"Failed to update YouTube content ID: {content.id}")
                except Exception as e:
                    print(f"Error updating YouTube content ID: {content.id}: {str(e)}")
                    self.content_context.update_content(
                        content.id, status=ContentStatus.ERROR
                    )
            else:
                print(
                    f"Failed to fetch transcript for YouTube content ID: {content.id}"
                )
                self.content_context.update_content(
                    content.id, status=ContentStatus.ERROR
                )

        self.session.close()
        print("YouTube transcript retrieval and update process completed.")


def get_youtube_transcripts(batch_size=None, delay=1):
    service = GetYoutubeTranscripts(batch_size, delay)
    service.get_and_update_transcripts()


if __name__ == "__main__":
    get_youtube_transcripts()
