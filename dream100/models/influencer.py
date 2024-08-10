from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from dream100.db_config import Base
from datetime import datetime

# Association table for the many-to-many relationship between Influencer and Project
influencer_project = Table(
    "influencer_project",
    Base.metadata,
    Column("influencer_id", Integer, ForeignKey("influencers.id")),
    Column("project_id", Integer, ForeignKey("projects.id")),
)


class Influencer(Base):
    """
    Represents an influencer in the influencer management system.

    An influencer can be associated with multiple projects.

    Attributes:
        id (int): The unique identifier for the influencer.
        name (str): The name of the influencer.
        created_at (datetime): The timestamp when the influencer was added to the system.
        updated_at (datetime): The timestamp when the influencer's information was last updated.
    """

    __tablename__ = "influencers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    projects = relationship(
        "Project", secondary=influencer_project, back_populates="influencers"
    )

    def __repr__(self):
        return f"<Influencer(id={self.id}, name='{self.name}')>"
