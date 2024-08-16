from colorama import Fore
from dream100_cli.renderer import (
    cli_render, cli_render_menu, cli_get_choice, cli_render_error, cli_input
)
import logging

logger = logging.getLogger(__name__)

def project_menu(project_context):
    while True:
        cli_render_menu("Project Management", [
            "Create Project",
            "List Projects",
            "Update Project",
            "Delete Project",
            "Back"
        ])
        
        choice = cli_get_choice([
            "Create Project",
            "List Projects",
            "Update Project",
            "Delete Project",
            "Back"
        ])
        
        if choice == 1:
            create_project(project_context)
        elif choice == 2:
            list_projects(project_context)
        elif choice == 3:
            update_project(project_context)
        elif choice == 4:
            delete_project(project_context)
        elif choice == 5:
            break
        else:
            cli_render_error("Invalid choice. Please try again.")

    cli_render("Returning to main menu...", Fore.CYAN)


def create_project(project_context):
    name = cli_input("Enter project name: ")
    description = cli_input("Enter project description: ")
    project = project_context.create_project(name, description)
    cli_render(f"Project created: {project}")


def list_projects(project_context):
    projects = project_context.list_projects()
    for project in projects:
        cli_render(
            f"ID: {project.id}, Name: {project.name}, Description: {project.description}"
        )


def update_project(project_context):
    project_id = int(cli_input("Enter project ID to update: "))
    name = cli_input("Enter new name (press enter to keep current): ")
    description = cli_input("Enter new description (press enter to keep current): ")
    project = project_context.update_project(
        project_id, name or None, description or None
    )
    if project:
        cli_render(f"Project updated: {project}")
    else:
        cli_render("Project not found.")


def delete_project(project_context):
    project_id = int(cli_input("Enter project ID to delete: "))
    if project_context.delete_project(project_id):
        cli_render("Project deleted successfully.")
    else:
        cli_render("Project not found or could not be deleted.")

if __name__ == "__main__":
    # Here you would initialize your contexts and pass them to project_menu
    # For example:
    # project_context = ProjectContext(session)
    # project_menu(project_context)
    pass
