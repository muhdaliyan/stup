"""arrange uv — Bootstrap a complete uv Python project."""

from arrange.utils import (
    check_uv,
    print_activate_hint,
    print_banner,
    print_done,
    run,
)


def run_command() -> None:
    """Execute the uv bootstrap sequence."""
    print_banner("uv", "Bootstrap a complete uv Python project")

    check_uv()

    # Initialize project
    run("uv init")

    # Pin Python version
    run("uv python pin 3.12")

    # Create virtual environment
    run("uv venv")

    # Show activation hint
    print_activate_hint()
    print_done()
