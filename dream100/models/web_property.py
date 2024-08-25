from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from dream100.db_config import Base
from enum import Enum as PyEnum


class WebPropertyType(PyEnum):
    FACEBOOK = "facebook"
    YOUTUBE = "youtube"
    LINKEDIN = "linkedin"
    WEBSITE = "website"
    TWITTER = "twitter"


class WebProperty(Base):
    """
    Represents a web property (website or social media account) associated with an influencer.

    Attributes:
        id (int): The unique identifier for the web property.
        influencer_id (int): The ID of the associated influencer.
        type (WebPropertyType): The type of web property (e.g., Facebook, YouTube).
        url (str): The URL of the web property.
        followers (int): The number of followers on the platform (if applicable).
    """

    __tablename__ = "web_properties"

    id = Column(Integer, primary_key=True)
    influencer_id = Column(Integer, ForeignKey("influencers.id"), nullable=False)
    type = Column(Enum(WebPropertyType), nullable=False)
    url = Column(String(255), nullable=False)
    followers = Column(Integer)

    influencer = relationship("Influencer", back_populates="web_properties")
    contents = relationship("Content", back_populates="web_property", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<WebProperty(id={self.id}, type={self.type},  url='{self.url}')>"
