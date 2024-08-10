from dream100.services import get_influencer_web_properties


def services_menu():
    while True:
        print("\n--- Services ---")
        print("1. Get Influencer Web Properties")
        print("2. Return to main menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            run_get_influencer_web_properties()
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")


def run_get_influencer_web_properties():
    get_influencer_web_properties()
