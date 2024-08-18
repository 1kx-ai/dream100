from dream100.models.web_property import WebPropertyType
from dream100_cli.renderer import cli_render, cli_input, cli_render_menu, cli_render_error
from colorama import Fore

def web_property_menu(web_property_context):
    while True:
        cli_render_menu("Web Property Management", [
            "Create a new web property",
            "List web properties",
            "Update a web property",
            "Delete a web property",
            "Return to main menu"
        ])
        choice = cli_input("Enter your choice")

        if choice == "1":
            create_web_property(web_property_context)
        elif choice == "2":
            list_web_properties(web_property_context)
        elif choice == "3":
            update_web_property(web_property_context)
        elif choice == "4":
            delete_web_property(web_property_context)
        elif choice == "5":
            break
        else:
            cli_render("Invalid choice. Please try again.", Fore.YELLOW)


def create_web_property(web_property_context):
    influencer_id = int(cli_input("Enter influencer ID"))
    cli_render("Available web property types:", Fore.CYAN)
    for type in WebPropertyType:
        cli_render(f"- {type.name}", Fore.CYAN)
    type = cli_input("Enter web property type")
    url = cli_input("Enter web property URL")
    followers = cli_input("Enter number of followers (optional, press enter to skip)")
    followers = int(followers) if followers else None

    try:
        web_property = web_property_context.create_web_property(
            influencer_id, type, url, followers
        )
        cli_render(f"Web property created: {web_property}", Fore.GREEN)
    except ValueError as e:
        cli_render_error(f"Error creating web property: {str(e)}")


def list_web_properties(web_property_context):
    influencer_id = cli_input("Enter influencer ID (optional, press enter to list all)")
    influencer_id = int(influencer_id) if influencer_id else None
    web_properties = web_property_context.list_web_properties(influencer_id)
    if web_properties:
        for wp in web_properties:
            cli_render(
                f"ID: {wp.id}, Influencer ID: {wp.influencer_id}, Type: {wp.type.name}, URL: {wp.url}, Followers: {wp.followers}",
                Fore.CYAN
            )
    else:
        cli_render("No web properties found.", Fore.YELLOW)


def update_web_property(web_property_context):
    web_property_id = int(cli_input("Enter web property ID to update"))
    cli_render("Available web property types:", Fore.CYAN)
    for type in WebPropertyType:
        cli_render(f"- {type.name}", Fore.CYAN)
    type = cli_input("Enter new type (press enter to keep current)")
    url = cli_input("Enter new URL (press enter to keep current)")
    followers = cli_input("Enter new number of followers (press enter to keep current)")
    followers = int(followers) if followers else None

    try:
        web_property = web_property_context.update_web_property(
            web_property_id, type or None, url or None, followers
        )
        if web_property:
            cli_render(f"Web property updated: {web_property}", Fore.GREEN)
        else:
            cli_render("Web property not found or update failed.", Fore.YELLOW)
    except ValueError as e:
        cli_render_error(f"Error updating web property: {str(e)}")


def delete_web_property(web_property_context):
    web_property_id = int(cli_input("Enter web property ID to delete"))
    if web_property_context.delete_web_property(web_property_id):
        cli_render("Web property deleted successfully.", Fore.GREEN)
    else:
        cli_render("Web property not found or could not be deleted.", Fore.YELLOW)
