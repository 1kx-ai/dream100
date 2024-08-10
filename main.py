import os
from dotenv import load_dotenv
from dream100.db_config import create_session, init_db
from dream100.projects.projects import ProjectContext
from dream100.influencers.influencers import InfluencerContext
from dream100.web_properties.web_properties import WebPropertyContext
from dream100.services import get_influencer_web_properties

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
    print("14. Get web properties for all influencers")
    print("15. Exit")
    return input("Enter your choice: ")


# Project functions
def create_project(project_context):
    name = input("Enter project name: ")
    description = input("Enter project description: ")
    project = project_context.create_project(name, description)
    print(f"Project created: {project}")


def list_projects(project_context):
    projects = project_context.list_projects()
    for project in projects:
        print(
            f"ID: {project.id}, Name: {project.name}, Description: {project.description}"
        )


def update_project(project_context):
    project_id = int(input("Enter project ID to update: "))
    name = input("Enter new name (press enter to keep current): ")
    description = input("Enter new description (press enter to keep current): ")
    project = project_context.update_project(
        project_id, name or None, description or None
    )
    if project:
        print(f"Project updated: {project}")
    else:
        print("Project not found.")


def delete_project(project_context):
    project_id = int(input("Enter project ID to delete: "))
    if project_context.delete_project(project_id):
        print("Project deleted successfully.")
    else:
        print("Project not found or could not be deleted.")


def create_influencer(influencer_context, project_context):
    name = input("Enter influencer name: ")
    projects = project_context.list_projects()
    print("Available projects:")
    for project in projects:
        print(f"ID: {project.id}, Name: {project.name}")
    project_ids = input("Enter project IDs for the influencer (comma-separated): ")
    project_id_list = [int(id.strip()) for id in project_ids.split(",") if id.strip()]
    influencer = influencer_context.create_influencer(name, project_id_list)
    print(f"Influencer created: {influencer}")


def list_influencers(influencer_context):
    influencers = influencer_context.list_influencers()
    for influencer in influencers:
        print(f"ID: {influencer.id}, Name: {influencer.name}")


def update_influencer(influencer_context, project_context):
    influencer_id = int(input("Enter influencer ID to update: "))
    name = input("Enter new name (press enter to keep current): ")
    projects = project_context.list_projects()
    print("Available projects:")
    for project in projects:
        print(f"ID: {project.id}, Name: {project.name}")
    project_ids = input(
        "Enter new project IDs (comma-separated, press enter to keep current): "
    )
    project_id_list = (
        [int(id.strip()) for id in project_ids.split(",") if id.strip()]
        if project_ids
        else None
    )
    influencer = influencer_context.update_influencer(
        influencer_id, name or None, project_id_list
    )
    if influencer:
        print(f"Influencer updated: {influencer}")
    else:
        print("Influencer not found.")


def delete_influencer(influencer_context):
    influencer_id = int(input("Enter influencer ID to delete: "))
    if influencer_context.delete_influencer(influencer_id):
        print("Influencer deleted successfully.")
    else:
        print("Influencer not found or could not be deleted.")


def get_influencer_projects(influencer_context):
    influencer_id = int(input("Enter influencer ID: "))
    projects = influencer_context.get_influencer_projects(influencer_id)
    if projects:
        for project in projects:
            print(f"Project ID: {project.id}, Name: {project.name}")
    else:
        print("No projects found for this influencer.")


# Web Property functions
def create_web_property(web_property_context, influencer_context):
    influencers = influencer_context.list_influencers()
    print("Available influencers:")
    for influencer in influencers:
        print(f"ID: {influencer.id}, Name: {influencer.name}")
    influencer_id = int(input("Enter influencer ID for the web property: "))
    url = input("Enter web property URL: ")
    type = input("Enter web property type: ")
    web_property = web_property_context.create_web_property(influencer_id, url, type)
    print(f"Web property created: {web_property}")


def list_web_properties(web_property_context):
    influencer_id = int(input("Enter influencer ID to list web properties: "))
    web_properties = web_property_context.list_web_properties(influencer_id)
    for web_property in web_properties:
        print(
            f"ID: {web_property.id}, URL: {web_property.url}, Type: {web_property.type}"
        )


def update_web_property(web_property_context):
    web_property_id = int(input("Enter web property ID to update: "))
    url = input("Enter new URL (press enter to keep current): ")
    type = input("Enter new type (press enter to keep current): ")
    web_property = web_property_context.update_web_property(
        web_property_id, url or None, type or None
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


def get_all_influencer_web_properties():
    print("Fetching web properties for all influencers...")
    get_influencer_web_properties()
    print("Web property fetch complete.")


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
            get_influencer_projects(influencer_context)
        elif choice == "10":
            create_web_property(web_property_context, influencer_context)
        elif choice == "11":
            list_web_properties(web_property_context)
        elif choice == "12":
            update_web_property(web_property_context)
        elif choice == "13":
            delete_web_property(web_property_context)
        elif choice == "14":
            get_all_influencer_web_properties()
        elif choice == "15":
            print("Exiting the application...")
            break
        else:
            print("Invalid choice. Please try again.")

    session.close()


if __name__ == "__main__":
    main()
