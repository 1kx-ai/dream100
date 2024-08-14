from dream100.models.web_property import WebPropertyType


def web_property_menu(web_property_context):
    while True:
        print("\n--- Web Property Management ---")
        print("1. Create a new web property")
        print("2. List web properties")
        print("3. Update a web property")
        print("4. Delete a web property")
        print("5. Return to main menu")
        choice = input("Enter your choice: ")

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
            print("Invalid choice. Please try again.")


def create_web_property(web_property_context):
    influencer_id = int(input("Enter influencer ID: "))
    print("Available web property types:")
    for type in WebPropertyType:
        print(f"- {type.name}")
    type = input("Enter web property type: ")
    url = input("Enter web property URL: ")
    followers = input("Enter number of followers (optional, press enter to skip): ")
    followers = int(followers) if followers else None

    try:
        web_property = web_property_context.create_web_property(
            influencer_id, type, url, followers
        )
        print(f"Web property created: {web_property}")
    except ValueError as e:
        print(f"Error creating web property: {str(e)}")


def list_web_properties(web_property_context):
    influencer_id = input("Enter influencer ID (optional, press enter to list all): ")
    influencer_id = int(influencer_id) if influencer_id else None
    web_properties = web_property_context.list_web_properties(influencer_id)
    if web_properties:
        for wp in web_properties:
            print(
                f"ID: {wp.id}, Influencer ID: {wp.influencer_id}, Type: {wp.type.name}, URL: {wp.url}, Followers: {wp.followers}"
            )
    else:
        print("No web properties found.")


def update_web_property(web_property_context):
    web_property_id = int(input("Enter web property ID to update: "))
    print("Available web property types:")
    for type in WebPropertyType:
        print(f"- {type.name}")
    type = input("Enter new type (press enter to keep current): ")
    url = input("Enter new URL (press enter to keep current): ")
    followers = input("Enter new number of followers (press enter to keep current): ")
    followers = int(followers) if followers else None

    try:
        web_property = web_property_context.update_web_property(
            web_property_id, type or None, url or None, followers
        )
        if web_property:
            print(f"Web property updated: {web_property}")
        else:
            print("Web property not found or update failed.")
    except ValueError as e:
        print(f"Error updating web property: {str(e)}")


def delete_web_property(web_property_context):
    web_property_id = int(input("Enter web property ID to delete: "))
    if web_property_context.delete_web_property(web_property_id):
        print("Web property deleted successfully.")
    else:
        print("Web property not found or could not be deleted.")
