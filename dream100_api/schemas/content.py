from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime


class ContentStatus(str, Enum):
    NONE = "none"
    OK = "ok"
    WARNING = "warning"
    ERROR = "error"


class ContentBase(BaseModel):
    link: str
    scraped_content: Optional[str] = None
    views: int = 0
    status: ContentStatus = ContentStatus.NONE


class ContentCreate(ContentBase):
    web_property_id: int


class Content(ContentBase):
    id: int
    web_property_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ContentUpdate(BaseModel):
    link: Optional[str] = None
    scraped_content: Optional[str] = None
    views: Optional[int] = None
    status: Optional[ContentStatus] = None


class ContentSearchResult(BaseModel):
    content: Content
    distance: float

    class Config:
        from_attributes = True


class ContentSearchResponse(BaseModel):
    contents: List[ContentSearchResult]
    total_count: int
    page: int
    per_page: int


class ContentPage(BaseModel):
    items: List[Content]
    total_count: int
    page: int
    per_page: int
