from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from dream100.db_config import Base
from enum import Enum as PyEnum


class ContentStatus(PyEnum):
    NONE = "none"
    OK = "ok"
    WARNING = "warning"
    ERROR = "error"


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True)
    web_property_id = Column(Integer, ForeignKey("web_properties.id"), nullable=False)
    link = Column(String(500), nullable=False)
    scraped_content = Column(Text)
    views = Column(Integer, default=0)
    status = Column(Enum(ContentStatus), default=ContentStatus.NONE, nullable=False)

    web_property = relationship(
        "WebProperty", back_populates="contents", single_parent=True
    )

    def __repr__(self):
        return f"<Content(id={self.id}, link='{self.link}', views={self.views}, status={self.status}, scraped_content={self.scraped_content[:100]})>"
