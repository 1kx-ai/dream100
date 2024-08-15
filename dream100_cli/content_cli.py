# content_cli.py

from .renderer import (
    cli_render, cli_input, cli_render_menu, cli_get_choice,
    cli_confirm, cli_render_table, cli_render_error
)
import logging

logger = logging.getLogger(__name__)

def content_menu(content_context):
    while True:
        cli_render_menu("Content Management", [
            "Add new content",
            "List all content",
            "Update content",
            "Delete content",
            "Return to main menu"
        ])
        choice = cli_get_choice(["Add new content", "List all content", "Update content", "Delete content", "Return to main menu"])
        
        if choice == 1:
            add_content(content_context)
        elif choice == 2:
            list_contents(content_context)
        elif choice == 3:
            update_content(content_context)
        elif choice == 4:
            delete_content(content_context)
        elif choice == 5:
            break
        else:
            cli_render_error("Invalid choice. Please try again.")

def add_content(content_context):
    web_property_id = int(cli_input("Enter web property ID"))
    link = cli_input("Enter content link")
    scraped_content = cli_input("Enter scraped content (optional)")
    views = int(cli_input("Enter number of views"))
    
    content = content_context.create_content(
        web_property_id, link, scraped_content, views
    )
    if content:
        cli_render(f"Content added: {content}")
    else:
        cli_render_error("Failed to add content. Web property not found.")

def list_contents(content_context):
    web_property_id = cli_input("Enter web property ID (or press Enter to list all)")
    web_property_id = int(web_property_id) if web_property_id else None
    contents = content_context.list_contents(web_property_id)
    
    if contents:
        headers = ["ID", "Link", "Views"]
        rows = [[content.id, content.link, content.views] for content in contents]
        cli_render_table(headers, rows)
    else:
        cli_render("No content found.")

def update_content(content_context):
    content_id = int(cli_input("Enter content ID to update"))
    link = cli_input("Enter new link (or press Enter to keep current)")
    scraped_content = cli_input("Enter new scraped content (or press Enter to keep current)")
    views = cli_input("Enter new number of views (or press Enter to keep current)")
    
    content = content_context.update_content(
        content_id, link or None, scraped_content or None, int(views) if views else None
    )
    if content:
        cli_render(f"Content updated: {content}")
    else:
        cli_render_error("Content not found or update failed.")

def delete_content(content_context):
    content_id = int(cli_input("Enter content ID to delete"))
    if cli_confirm("Are you sure you want to delete this content?"):
        if content_context.delete_content(content_id):
            cli_render("Content deleted successfully.")
        else:
            cli_render_error("Content not found or could not be deleted.")
    else:
        cli_render("Deletion cancelled.")