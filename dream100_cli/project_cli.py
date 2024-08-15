from dream100_cli.renderer import (
    cli_render, cli_render_menu, cli_get_choice, cli_render_error
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
    cli_render("Creating a new project...", Fore.CYAN)
    # Implementation for creating a project

def list_projects(project_context):
    cli_render("Listing all projects...", Fore.CYAN)
    # Implementation for listing projects

def update_project(project_context):
    cli_render("Updating a project...", Fore.CYAN)
    # Implementation for updating a project

def delete_project(project_context):
    cli_render("Deleting a project...", Fore.CYAN)
    # Implementation for deleting a project

if __name__ == "__main__":
    # Here you would initialize your contexts and pass them to project_menu
    # For example:
    # project_context = ProjectContext(session)
    # project_menu(project_context)
    pass
