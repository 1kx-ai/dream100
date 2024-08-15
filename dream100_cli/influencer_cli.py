# influencer_cli.py

from .renderer import (
    cli_render, cli_input, cli_render_menu, cli_get_choice,
    cli_confirm, cli_render_table, cli_render_error
)
import logging

logger = logging.getLogger(__name__)

def influencer_menu(influencer_context, project_context):
    while True:
        cli_render_menu("Influencer Management", [
            "Create a new influencer",
            "List all influencers",
            "Update an influencer",
            "Delete an influencer",
            "View influencer's projects",
            "Return to main menu"
        ])
        choice = cli_get_choice([
            "Create a new influencer",
            "List all influencers",
            "Update an influencer",
            "Delete an influencer",
            "View influencer's projects",
            "Return to main menu"
        ])
        
        if choice == 1:
            create_influencer(influencer_context, project_context)
        elif choice == 2:
            list_influencers(influencer_context)
        elif choice == 3:
            update_influencer(influencer_context, project_context)
        elif choice == 4:
            delete_influencer(influencer_context)
        elif choice == 5:
            view_influencer_projects(influencer_context)
        elif choice == 6:
            break
        else:
            cli_render_error("Invalid choice. Please try again.")

def create_influencer(influencer_context, project_context):
    name = cli_input("Enter influencer name")
    projects = project_context.list_projects()
    
    cli_render("Available projects:")
    headers = ["ID", "Name"]
    rows = [[project.id, project.name] for project in projects]
    cli_render_table(headers, rows)
    
    project_ids_input = cli_input("Enter project IDs (comma-separated) to add the influencer to")
    project_ids = [int(id.strip()) for id in project_ids_input.split(",") if id.strip()]
    
    influencer = influencer_context.create_influencer(name, project_ids)
    cli_render(f"Influencer created: {influencer}")

def list_influencers(influencer_context):
    influencers = influencer_context.list_influencers()
    headers = ["ID", "Name"]
    rows = [[influencer.id, influencer.name] for influencer in influencers]
    cli_render_table(headers, rows)

def update_influencer(influencer_context, project_context):
    influencer_id = int(cli_input("Enter influencer ID to update"))
    name = cli_input("Enter new name (press enter to keep current)")
    projects = project_context.list_projects()
    
    cli_render("Available projects:")
    headers = ["ID", "Name"]
    rows = [[project.id, project.name] for project in projects]
    cli_render_table(headers, rows)
    
    project_ids_input = cli_input("Enter new project IDs (comma-separated) to associate the influencer with (press enter to keep current)")
    project_ids = (
        [int(id.strip()) for id in project_ids_input.split(",") if id.strip()]
        if project_ids_input
        else None
    )
    
    influencer = influencer_context.update_influencer(
        influencer_id, name or None, project_ids
    )
    if influencer:
        cli_render(f"Influencer updated: {influencer}")
    else:
        cli_render_error("Influencer not found.")

def delete_influencer(influencer_context):
    influencer_id = int(cli_input("Enter influencer ID to delete"))
    if cli_confirm("Are you sure you want to delete this influencer?"):
        if influencer_context.delete_influencer(influencer_id):
            cli_render("Influencer deleted successfully.")
        else:
            cli_render_error("Influencer not found or could not be deleted.")
    else:
        cli_render("Deletion cancelled.")

def view_influencer_projects(influencer_context):
    influencer_id = int(cli_input("Enter influencer ID"))
    projects = influencer_context.get_influencer_projects(influencer_id)
    if projects:
        cli_render(f"Projects for influencer (ID: {influencer_id}):")
        headers = ["ID", "Name"]
        rows = [[project.id, project.name] for project in projects]
        cli_render_table(headers, rows)
    else:
        cli_render_error("Influencer not found or not associated with any projects.")