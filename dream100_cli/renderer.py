# cli_utils.py

import logging
from typing import List, Any, Optional
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init()

logger = logging.getLogger(__name__)

def cli_render(message: str, color: Optional[str] = None) -> None:
    """
    Render a message to the CLI with optional color.

    Args:
        message (str): The message to render.
        color (Optional[str]): Color of the message. Use Fore colors from colorama.
    """
    if color:
        print(f"{color}{message}{Style.RESET_ALL}")
    else:
        print(message)

def cli_input(prompt: str) -> str:
    """
    Get input from the user with a prompt.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        str: The user's input.
    """
    return input(f"{prompt}: ")

def cli_render_menu(title: str, options: List[str]) -> None:
    """
    Render a menu with a title and numbered options.

    Args:
        title (str): The title of the menu.
        options (List[str]): A list of menu options.
    """
    cli_render(f"\n--- {title} ---", Fore.CYAN)
    for i, option in enumerate(options, 1):
        cli_render(f"{i}. {option}")

def cli_get_choice(options: List[str]) -> int:
    """
    Get a valid choice from the user based on a list of options.

    Args:
        options (List[str]): A list of options.

    Returns:
        int: The index of the chosen option.
    """
    while True:
        try:
            choice = int(cli_input("Enter your choice"))
            if 1 <= choice <= len(options):
                return choice
            cli_render("Invalid choice. Please try again.", Fore.YELLOW)
        except ValueError:
            cli_render("Please enter a number.", Fore.YELLOW)

def cli_confirm(prompt: str) -> bool:
    """
    Ask the user for confirmation.

    Args:
        prompt (str): The confirmation prompt.

    Returns:
        bool: True if confirmed, False otherwise.
    """
    response = cli_input(f"{prompt} (y/n)").lower()
    return response in ['y', 'yes']

def cli_render_table(headers: List[str], rows: List[List[Any]]) -> None:
    """
    Render a simple table in the CLI.

    Args:
        headers (List[str]): The table headers.
        rows (List[List[Any]]): The table rows.
    """
    # Calculate column widths
    widths = [max(len(str(cell)) for cell in col) for col in zip(headers, *rows)]
    
    # Render headers
    header_row = " | ".join(f"{header:<{width}}" for header, width in zip(headers, widths))
    cli_render(header_row, Fore.GREEN)
    cli_render("-" * len(header_row), Fore.GREEN)
    
    # Render rows
    for row in rows:
        cli_render(" | ".join(f"{str(cell):<{width}}" for cell, width in zip(row, widths)))

def cli_render_error(message: str) -> None:
    """
    Render an error message to the CLI.

    Args:
        message (str): The error message to render.
    """
    cli_render(f"Error: {message}", Fore.RED)
    logger.error(message)

# Example usage
if __name__ == "__main__":
    cli_render("Welcome to the CLI Utils demo!", Fore.CYAN)
    cli_render_menu("Main Menu", ["Option 1", "Option 2", "Exit"])
    choice = cli_get_choice(["Option 1", "Option 2", "Exit"])
    cli_render(f"You chose option {choice}")
    
    if cli_confirm("Do you want to see a table?"):
        headers = ["Name", "Age", "City"]
        rows = [
            ["Alice", 30, "New York"],
            ["Bob", 25, "Los Angeles"],
            ["Charlie", 35, "Chicago"]
        ]
        cli_render_table(headers, rows)
    
    cli_render_error("This is a sample error message")