import os
from dotenv import load_dotenv
from dream100.db_config import create_session, init_db, Base
from dream100.projects.projects import ProjectContext
from dream100.influencers.influencers import InfluencerContext
from dream100.web_properties.web_property_context import WebPropertyContext
from dream100.contents.contents import ContentContext
from dream100_cli.main_cli import main_menu
from sqlalchemy import inspect

load_dotenv()


def revert_database(session, engine):
    inspector = inspect(engine)

    if inspector.get_table_names():
        print("Dropping all tables...")
        Base.metadata.drop_all(engine, checkfirst=True)
        print("All tables dropped.")

    print("Recreating all tables...")
    Base.metadata.create_all(engine)
    print("All tables recreated.")

    print("Database reverted successfully.")


def main():
    session, engine = create_session()
    init_db(engine)
    project_context = ProjectContext(session)
    influencer_context = InfluencerContext(session)
    web_property_context = WebPropertyContext(session)
    content_context = ContentContext(session)

    while True:
        print("\n--- Influencer Project Management ---")
        print("1. Enter main menu")
        print("2. Revert database (drop and recreate all tables)")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            main_menu(
                project_context,
                influencer_context,
                web_property_context,
                content_context,
            )
        elif choice == "2":
            confirm = input("This will delete all data. Are you sure? (y/n): ")
            if confirm.lower() == "y":
                revert_database(session, engine)
                # Recreate contexts with new session
                session.close()
                session, engine = create_session()
                project_context = ProjectContext(session)
                influencer_context = InfluencerContext(session)
                content_context = ContentContext(session)
            else:
                print("Database revert cancelled.")
        elif choice == "3":
            print("Exiting the application...")
            break
        else:
            print("Invalid choice. Please try again.")

    session.close()


if __name__ == "__main__":
    main()
