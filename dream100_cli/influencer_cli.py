def influencer_menu(influencer_context, project_context):
    while True:
        print("\n--- Influencer Management ---")
        print("1. Create a new influencer")
        print("2. List all influencers")
        print("3. Update an influencer")
        print("4. Delete an influencer")
        print("5. View influencer's projects")
        print("6. Return to main menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_influencer(influencer_context, project_context)
        elif choice == "2":
            list_influencers(influencer_context)
        elif choice == "3":
            update_influencer(influencer_context, project_context)
        elif choice == "4":
            delete_influencer(influencer_context)
        elif choice == "5":
            view_influencer_projects(influencer_context)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


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
