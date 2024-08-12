from dream100.services import (
    get_influencer_web_properties,
    get_influencer_youtube_links,
    get_youtube_transcripts,
)


def services_menu():
    while True:
        print("\n--- Services ---")
        print("1. Get Influencer Web Properties")
        print("2. Get YouTube Links")
        print("3. Get YouTube Transcripts")
        print("4. Return to main menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            run_get_influencer_web_properties()
        elif choice == "2":
            run_get_youtube_links()
        elif choice == "3":
            run_get_youtube_transcripts()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")


def run_get_influencer_web_properties():
    get_influencer_web_properties()


def run_get_youtube_links():
    get_influencer_youtube_links()


def run_get_youtube_transcripts():
    get_youtube_transcripts()


if __name__ == "__main__":
    services_menu()
