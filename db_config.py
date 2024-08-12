import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

Base = declarative_base()


def get_database_url():
    """Construct database URL from environment variables"""
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    if not all([db_username, db_password, db_host, db_port, db_name]):
        raise ValueError("Missing database configuration. Please check your .env file.")

    return f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"


def create_session():
    """Create a new database session"""
    engine = create_engine(get_database_url())
    Session = sessionmaker(bind=engine)
    return Session(), engine


def init_db(engine):
    """Initialize the database by creating all tables and ensuring the vector extension is installed"""
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()

    Base.metadata.create_all(engine)
