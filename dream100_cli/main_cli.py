from dream100_cli.project_cli import project_menu
from dream100_cli.influencer_cli import influencer_menu
from dream100_cli.web_property_cli import web_property_menu
from dream100_cli.content_cli import content_menu
from dream100_cli.services_cli import services_menu


def main_menu(
    project_context, influencer_context, web_property_context, content_context
):
    while True:
        print("\n--- Influencer Project Management ---")
        print("1. Project Management")
        print("2. Influencer Management")
        print("3. Web Property Management")
        print("4. Content Management")
        print("5. Services")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            project_menu(project_context)
        elif choice == "2":
            influencer_menu(influencer_context, project_context)
        elif choice == "3":
            web_property_menu(web_property_context)
        elif choice == "4":
            content_menu(content_context)
        elif choice == "5":
            services_menu()
        elif choice == "6":
            print("Exiting the application...")
            break
        else:
            print("Invalid choice. Please try again.")
