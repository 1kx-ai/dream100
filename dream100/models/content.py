from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from dream100.db_config import Base


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True)
    web_property_id = Column(Integer, ForeignKey("web_properties.id"), nullable=False)
    link = Column(String(500), nullable=False)
    scraped_content = Column(Text)
    views = Column(Integer, default=0)

    web_property = relationship("WebProperty", back_populates="contents")

    def __repr__(self):
        return f"<Content(id={self.id}, link='{self.link}', views={self.views})>"
