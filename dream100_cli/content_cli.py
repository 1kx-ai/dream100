def content_menu(content_context):
    while True:
        print("\n--- Content Management ---")
        print("1. Add new content")
        print("2. List all content")
        print("3. Update content")
        print("4. Delete content")
        print("5. Return to main menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_content(content_context)
        elif choice == "2":
            list_contents(content_context)
        elif choice == "3":
            update_content(content_context)
        elif choice == "4":
            delete_content(content_context)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def add_content(content_context):
    web_property_id = int(input("Enter web property ID: "))
    link = input("Enter content link: ")
    scraped_content = input("Enter scraped content (optional): ")
    views = int(input("Enter number of views: "))
    content = content_context.create_content(
        web_property_id, link, scraped_content, views
    )
    if content:
        print(f"Content added: {content}")
    else:
        print("Failed to add content. Web property not found.")


def list_contents(content_context):
    web_property_id = input("Enter web property ID (or press Enter to list all): ")
    web_property_id = int(web_property_id) if web_property_id else None
    contents = content_context.list_contents(web_property_id)
    if contents:
        for content in contents:
            print(f"ID: {content.id}, Link: {content.link}, Views: {content.views}")
    else:
        print("No content found.")


def update_content(content_context):
    content_id = int(input("Enter content ID to update: "))
    link = input("Enter new link (or press Enter to keep current): ")
    scraped_content = input(
        "Enter new scraped content (or press Enter to keep current): "
    )
    views = input("Enter new number of views (or press Enter to keep current): ")

    content = content_context.update_content(
        content_id, link or None, scraped_content or None, int(views) if views else None
    )
    if content:
        print(f"Content updated: {content}")
    else:
        print("Content not found or update failed.")


def delete_content(content_context):
    content_id = int(input("Enter content ID to delete: "))
    if content_context.delete_content(content_id):
        print("Content deleted successfully.")
    else:
        print("Content not found or could not be deleted.")
