import os
from googleapiclient.discovery import build
from urllib.parse import urlparse
import time
from dream100.db_config import create_session
from dream100.context.web_properties import WebPropertyContext
from dream100.context.contents import ContentContext
from dream100.models.web_property import WebPropertyType
from config import config
import logging

logger = logging.getLogger(__name__)


class GetYouTubeLinksService:
    def __init__(self):
        self.api_key = config.GOOGLE_API_KEY
        if not self.api_key:
            raise ValueError("Please set a valid GOOGLE_API_KEY in your .env file")

        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.session, _ = create_session()
        self.web_property_context = WebPropertyContext(self.session)
        self.content_context = ContentContext(self.session)

    def get_channel_id_from_url(self, url):
        parsed_url = urlparse(url)
        if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
            if "/channel/" in parsed_url.path:
                return parsed_url.path.split("/")[-1]
            elif parsed_url.path.startswith("/user/"):
                username = parsed_url.path.split("/")[-1]
                response = (
                    self.youtube.channels()
                    .list(part="id", forUsername=username)
                    .execute()
                )
                if "items" in response:
                    return response["items"][0]["id"]
            elif parsed_url.path.startswith("/c/") or parsed_url.path.startswith("/@"):
                # Handle both /c/ and /@ URLs
                custom_name = parsed_url.path.split("/")[-1]
                response = (
                    self.youtube.search()
                    .list(part="id", q=custom_name, type="channel")
                    .execute()
                )
                if "items" in response:
                    return response["items"][0]["id"]["channelId"]
        return None

    def get_channel_videos(self, channel_url):
        channel_id = self.get_channel_id_from_url(channel_url)
        if not channel_id:
            logger.info(
                f"Invalid channel URL or unable to find channel ID: {channel_url}"
            )
            return []

        video_links = []
        request = self.youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            maxResults=50,
            type="video",
        )

        while request:
            response = request.execute()
            for item in response["items"]:
                video_id = item["id"]["videoId"]
                video_link = f"https://www.youtube.com/watch?v={video_id}"
                video_links.append(video_link)
            request = self.youtube.search().list_next(request, response)

        return video_links

    def process_youtube_links(self):
        youtube_properties = self.web_property_context.list_web_properties()
        youtube_properties = [
            wp for wp in youtube_properties if wp.type == WebPropertyType.YOUTUBE
        ]

        for web_property in youtube_properties:
            logger.info(
                f"Processing YouTube channel for influencer ID {web_property.influencer_id}..."
            )
            youtube_videos = self.get_channel_videos(web_property.url)

            if youtube_videos:
                for video_link in youtube_videos:
                    existing_content = self.content_context.list_contents(
                        web_property.id
                    )
                    if not any(
                        content.link == video_link for content in existing_content
                    ):
                        self.content_context.create_content(
                            web_property_id=web_property.id, link=video_link
                        )
                logger.info(
                    f"Found {len(youtube_videos)} videos for influencer ID {web_property.influencer_id}"
                )
            else:
                logger.info(
                    f"No videos found for influencer ID {web_property.influencer_id}"
                )

            # Add a delay to avoid hitting rate limits
            time.sleep(1)

        self.session.close()
        logger.info("Processing complete.")


def get_influencer_youtube_links():
    service = GetYouTubeLinksService()
    service.process_youtube_links()


if __name__ == "__main__":
    get_influencer_youtube_links()
