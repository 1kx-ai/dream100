import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
import sys

# Load environment variables
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


def create_connection():
    """Create a database connection using SQLAlchemy and environment variables"""
    try:
        db_url = get_database_url()
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        print("Successfully connected to the database using SQLAlchemy.")
        return session, engine
    except SQLAlchemyError as e:
        print(f"Error connecting to database: {e}")
        return None, None
    except ValueError as e:
        print(f"Configuration error: {e}")
        return None, None


def close_connection(session):
    """Close the database session"""
    if session:
        session.close()
        print("Database session closed.")


def main_menu():
    """Display the main menu and get user input"""
    print("\n--- Influencer Project Management ---")
    print("1. Exit")
    # Add more menu options here as we develop the application
    choice = input("Enter your choice: ")
    return choice


def main():
    # Set up logging
    log_level = os.getenv("LOG_LEVEL", "INFO")
    # TODO: Set up proper logging configuration here

    # Check if we're in debug mode
    debug_mode = os.getenv("DEBUG", "False").lower() == "true"

    session, engine = create_connection()
    if session is None or engine is None:
        print("Error! Cannot create the database connection.")
        return

    # Create all tables stored in this metadata
    Base.metadata.create_all(engine)

    while True:
        choice = main_menu()
        if choice == "1":
            print("Exiting the application...")
            break
        else:
            print("Invalid choice. Please try again.")

    close_connection(session)


if __name__ == "__main__":
    main()
