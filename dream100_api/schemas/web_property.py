from pydantic import BaseModel
from enum import Enum
from typing import Optional, List

class WebPropertyType(str, Enum):
    FACEBOOK = "facebook"
    YOUTUBE = "youtube"
    LINKEDIN = "linkedin"
    WEBSITE = "website"
    TWITTER = "twitter"

class WebPropertyBase(BaseModel):
    influencer_id: int
    type: WebPropertyType
    url: str
    followers: Optional[int] = None

class WebPropertyCreate(WebPropertyBase):
    pass

class WebPropertyUpdate(BaseModel):
    type: Optional[WebPropertyType] = None
    url: Optional[str] = None
    followers: Optional[int] = None

class WebProperty(WebPropertyBase):
    id: int

    class Config:
        from_attributes = True

class PaginatedWebProperties(BaseModel):
    items: List[WebProperty]
    total: int
    page: int
    per_page: int
    pages: int
