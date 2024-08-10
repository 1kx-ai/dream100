import os
from dotenv import load_dotenv
from dream100.db_config import create_session, init_db, Base
from dream100.projects.projects import ProjectContext
from dream100.influencers.influencers import InfluencerContext
from dream100.web_properties.web_properties import WebPropertyContext
from sqlalchemy import inspect
from dream100.models.project import Project
from dream100.models.influencer import Influencer
from dream100.models.web_property import WebProperty, WebPropertyType

load_dotenv()


def main_menu():
    print("\n--- Influencer Project Management ---")
    print("1. Create a new project")
    print("2. List all projects")
    print("3. Update a project")
    print("4. Delete a project")
    print("5. Create a new influencer")
    print("6. List all influencers")
    print("7. Update an influencer")
    print("8. Delete an influencer")
    print("9. View influencer's projects")
    print("10. Add web property to influencer")
    print("11. List influencer's web properties")
    print("12. Update web property")
    print("13. Delete web property")
    print("14. Revert database (drop and recreate all tables)")
    print("15. Exit")
    return input("Enter your choice: ")


# ... (keep existing functions)


def add_web_property(web_property_context, influencer_context):
    influencer_id = int(input("Enter influencer ID: "))
    influencer = influencer_context.get_influencer(influencer_id)
    if not influencer:
        print("Influencer not found.")
        return

    print("Web property types:")
    for type in WebPropertyType:
        print(f"- {type.value}")

    type = input("Enter web property type: ")
    url = input("Enter URL: ")
    followers = input("Enter number of followers (press enter to skip): ")
    followers = int(followers) if followers else None

    web_property = web_property_context.create_web_property(
        influencer_id, type, url, followers
    )
    print(f"Web property added: {web_property}")


def list_web_properties(web_property_context):
    influencer_id = input("Enter influencer ID (press enter to list all): ")
    influencer_id = int(influencer_id) if influencer_id else None
    web_properties = web_property_context.list_web_properties(influencer_id)
    for web_property in web_properties:
        print(
            f"ID: {web_property.id}, Type: {web_property.type.value}, URL: {web_property.url}, Followers: {web_property.followers}"
        )


def update_web_property(web_property_context):
    web_property_id = int(input("Enter web property ID to update: "))
    type = input("Enter new type (press enter to keep current): ")
    url = input("Enter new URL (press enter to keep current): ")
    followers = input("Enter new number of followers (press enter to keep current): ")
    followers = int(followers) if followers else None

    web_property = web_property_context.update_web_property(
        web_property_id, type or None, url or None, followers
    )
    if web_property:
        print(f"Web property updated: {web_property}")
    else:
        print("Web property not found.")


def delete_web_property(web_property_context):
    web_property_id = int(input("Enter web property ID to delete: "))
    if web_property_context.delete_web_property(web_property_id):
        print("Web property deleted successfully.")
    else:
        print("Web property not found or could not be deleted.")


def main():
    session, engine = create_session()
    init_db(engine)
    project_context = ProjectContext(session)
    influencer_context = InfluencerContext(session)
    web_property_context = WebPropertyContext(session)

    while True:
        choice = main_menu()
        if choice == "1":
            create_project(project_context)
        elif choice == "2":
            list_projects(project_context)
        elif choice == "3":
            update_project(project_context)
        elif choice == "4":
            delete_project(project_context)
        elif choice == "5":
            create_influencer(influencer_context, project_context)
        elif choice == "6":
            list_influencers(influencer_context)
        elif choice == "7":
            update_influencer(influencer_context, project_context)
        elif choice == "8":
            delete_influencer(influencer_context)
        elif choice == "9":
            view_influencer_projects(influencer_context)
        elif choice == "10":
            add_web_property(web_property_context, influencer_context)
        elif choice == "11":
            list_web_properties(web_property_context)
        elif choice == "12":
            update_web_property(web_property_context)
        elif choice == "13":
            delete_web_property(web_property_context)
        elif choice == "14":
            confirm = input("This will delete all data. Are you sure? (y/n): ")
            if confirm.lower() == "y":
                revert_database(session, engine)
                # Recreate contexts with new session
                session.close()
                session, engine = create_session()
                project_context = ProjectContext(session)
                influencer_context = InfluencerContext(session)
                web_property_context = WebPropertyContext(session)
            else:
                print("Database revert cancelled.")
        elif choice == "15":
            print("Exiting the application...")
            break
        else:
            print("Invalid choice. Please try again.")

    session.close()


if __name__ == "__main__":
    main()
