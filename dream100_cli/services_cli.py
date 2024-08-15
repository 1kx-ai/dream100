from dream100_cli.renderer import cli_render, cli_input, cli_render_menu, cli_get_choice
from dream100.services import (
    get_influencer_web_properties,
    get_influencer_youtube_links,
    get_youtube_transcripts,
    embed_youtube_transcripts,
)


def services_menu():
    while True:
        cli_render_menu("Services", [
            "Get Influencer Web Properties",
            "Get YouTube Links",
            "Get YouTube Transcripts",
            "Embed YouTube Transcripts",
            "Return to main menu"
        ])
        choice = cli_get_choice([
            "Get Influencer Web Properties",
            "Get YouTube Links",
            "Get YouTube Transcripts",
            "Embed YouTube Transcripts",
            "Return to main menu"
        ])

        if choice == "1":
            run_get_influencer_web_properties()
        elif choice == "2":
            run_get_youtube_links()
        elif choice == "3":
            run_get_youtube_transcripts()
        elif choice == "4":
            run_embed_youtube_transcripts()
        elif choice == "5":
            break
        else:
            cli_render("Invalid choice. Please try again.", Fore.YELLOW)


def run_get_influencer_web_properties():
    get_influencer_web_properties()


def run_get_youtube_links():
    get_influencer_youtube_links()


def run_get_youtube_transcripts():
    get_youtube_transcripts()


def run_embed_youtube_transcripts():
    batch_size = int(cli_input("Enter batch size (default is 100)") or 100)
    embed_youtube_transcripts(batch_size)


if __name__ == "__main__":
    services_menu()
