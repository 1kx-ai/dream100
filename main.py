import os
from dotenv import load_dotenv
from dream100.db_config import create_session, init_db, Base
from dream100.projects.projects import ProjectContext
from dream100.influencers.influencers import InfluencerContext
from sqlalchemy import inspect
from dream100.models.project import Project
from dream100.models.influencer import Influencer

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
    print("10. Revert database (drop and recreate all tables)")
    print("11. Exit")
    return input("Enter your choice: ")


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
    project_ids = input(
        "Enter project IDs (comma-separated) to add the influencer to: "
    )
    project_ids = [int(id.strip()) for id in project_ids.split(",") if id.strip()]
    influencer = influencer_context.create_influencer(name, project_ids)
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
        "Enter new project IDs (comma-separated) to associate the influencer with (press enter to keep current): "
    )
    project_ids = (
        [int(id.strip()) for id in project_ids.split(",") if id.strip()]
        if project_ids
        else None
    )
    influencer = influencer_context.update_influencer(
        influencer_id, name or None, project_ids
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


def view_influencer_projects(influencer_context):
    influencer_id = int(input("Enter influencer ID: "))
    projects = influencer_context.get_influencer_projects(influencer_id)
    if projects:
        print(f"Projects for influencer (ID: {influencer_id}):")
        for project in projects:
            print(f"ID: {project.id}, Name: {project.name}")
    else:
        print("Influencer not found or not associated with any projects.")


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
            confirm = input("This will delete all data. Are you sure? (y/n): ")
            if confirm.lower() == "y":
                revert_database(session, engine)
                # Recreate contexts with new session
                session.close()
                session, engine = create_session()
                project_context = ProjectContext(session)
                influencer_context = InfluencerContext(session)
            else:
                print("Database revert cancelled.")
        elif choice == "11":
            print("Exiting the application...")
            break
        else:
            print("Invalid choice. Please try again.")

    session.close()


if __name__ == "__main__":
    main()
