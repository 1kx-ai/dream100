import os
from dotenv import load_dotenv
from dream100.db_config import create_session, init_db
from dream100.projects.projects import ProjectContext

load_dotenv()


def main_menu():
    print("\n--- Influencer Project Management ---")
    print("1. Create a new project")
    print("2. List all projects")
    print("3. Update a project")
    print("4. Delete a project")
    print("5. Exit")
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


def main():
    session, engine = create_session()
    init_db(engine)
    project_context = ProjectContext(session)

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
            print("Exiting the application...")
            break
        else:
            print("Invalid choice. Please try again.")

    session.close()


if __name__ == "__main__":
    main()
