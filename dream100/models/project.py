from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from dream100.db_config import Base
from datetime import datetime


class Project(Base):
    """
    Represents a project in the influencer management system.

    A project can have multiple influencers associated with it.
    It serves as a way to organize and group influencers for specific campaigns or initiatives.

    Attributes:
        id (int): The unique identifier for the project.
        name (str): The name of the project.
        description (str): A brief description of the project.
        created_at (datetime): The timestamp when the project was created.
        updated_at (datetime): The timestamp when the project was last updated.
    """

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # This will be used when we implement the Influencer model
    # influencers = relationship("Influencer", back_populates="project")

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"
