from colorama import Fore

from dream100_cli.project_cli import project_menu
from dream100_cli.influencer_cli import influencer_menu
from dream100_cli.web_property_cli import web_property_menu
from dream100_cli.content_cli import content_menu
from dream100_cli.services_cli import services_menu
from dream100_cli.renderer import (
    cli_render, cli_render_menu, cli_get_choice, cli_render_error
)
import logging

logger = logging.getLogger(__name__)

def main_menu(
    project_context, influencer_context, web_property_context, content_context
):
    while True:
        cli_render_menu("Influencer Project Management", [
            "Project Management",
            "Influencer Management",
            "Web Property Management",
            "Content Management",
            "Services",
            "Exit"
        ])
        
        choice = cli_get_choice([
            "Project Management",
            "Influencer Management",
            "Web Property Management",
            "Content Management",
            "Services",
            "Exit"
        ])
        
        if choice == 1:
            project_menu(project_context)
        elif choice == 2:
            influencer_menu(influencer_context, project_context)
        elif choice == 3:
            web_property_menu(web_property_context)
        elif choice == 4:
            content_menu(content_context)
        elif choice == 5:
            services_menu()
        elif choice == 6:
            cli_render("Exiting the application...", Fore.CYAN)
            break
        else:
            cli_render_error("Invalid choice. Please try again.")

    cli_render("Application exited", Fore.CYAN)

if __name__ == "__main__":
    # Here you would initialize your contexts and pass them to main_menu
    # For example:
    # project_context = ProjectContext(session)
    # influencer_context = InfluencerContext(session)
    # web_property_context = WebPropertyContext(session)
    # content_context = ContentContext(session)
    # main_menu(project_context, influencer_context, web_property_context, content_context)
    pass
