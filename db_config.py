from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import config

Base = declarative_base()

def create_session():
    """Create a new database session"""
    engine = create_engine(config.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session(), engine

def init_db(engine):
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(engine)