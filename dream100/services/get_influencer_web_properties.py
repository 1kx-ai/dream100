import os
import requests
from urllib.parse import urlparse
import time
from dotenv import load_dotenv
from dream100.db_config import create_session
from dream100.influencers.influencers import InfluencerContext
from dream100.web_properties.web_properties import WebPropertyContext
from dream100.models.web_property import WebProperty, WebPropertyType
from config import config

class InfluencerWebPropertiesService:
    def __init__(self):
        self.api_key = config.GOOGLE_API_KEY
        self.cx = config.GOOGLE_SEARCH_ENGINE_ID
        if not self.api_key or not self.cx:
            raise ValueError("Please set valid GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID in your .env file")

        self.session, _ = create_session()
        self.influencer_context = InfluencerContext(self.session)
        self.web_property_context = WebPropertyContext(self.session)

    def google_search(self, query, **kwargs):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {"q": query, "key": self.api_key, "cx": self.cx, **kwargs}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Search query failed: {response.status_code}")

    def find_website(self, query):
        search_results = self.google_search(query + " website")
        items = search_results.get("items", [])
        return items[0]["link"] if items else None

    def find_social_media_page(self, query, platform):
        search_results = self.google_search(query + " " + platform)
        def is_platform_link(item):
            parsed = urlparse(item["link"])
            return f"{platform}.com" in parsed.netloc
        items = search_results.get("items", [])
        platform_links = list(filter(is_platform_link, items))
        return platform_links[0]["link"] if platform_links else None

    def find_links(self, influencer, existing_properties):
        query = influencer.name
        existing_types = [prop.type for prop in existing_properties]

        if WebPropertyType.WEBSITE not in existing_types:
            website = self.find_website(query)
            if website:
                self.web_property_context.create_web_property(
                    influencer_id=influencer.id,
                    type=WebPropertyType.WEBSITE.value,
                    url=website
                )
                print(f"Added website for {influencer.name}: {website}")

        for platform in ["facebook", "twitter", "youtube", "linkedin"]:
            platform_type = getattr(WebPropertyType, platform.upper())
            if platform_type not in existing_types:
                social_link = self.find_social_media_page(query, platform)
                if social_link:
                    self.web_property_context.create_web_property(
                        influencer_id=influencer.id,
                        type=platform_type.value,
                        url=social_link
                    )
                    print(f"Added {platform} for {influencer.name}: {social_link}")

    def get_web_properties(self):
        influencers = self.influencer_context.list_influencers()

        for influencer in influencers:
            existing_properties = self.web_property_context.list_web_properties(influencer.id)
            if len(existing_properties) < 5:  # 5 is the max (website + 4 social platforms)
                try:
                    self.find_links(influencer, existing_properties)
                    print(f"Processed influencer: {influencer.name}")
                except Exception as e:
                    print(f"Error processing influencer {influencer.name}: {str(e)}")
                    self.session.rollback()
                    continue
                # Add a delay to avoid hitting API rate limits
                time.sleep(1)
            else:
                print(f"Skipping {influencer.name}: All web properties already exist")

        self.session.close()
        print("Processing complete.")

def get_influencer_web_properties():
    service = InfluencerWebPropertiesService()
    service.get_web_properties()

if __name__ == "__main__":
    get_influencer_web_properties()
