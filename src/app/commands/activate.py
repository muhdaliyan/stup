"""stup activate — Smart cross-platform venv activator."""

from app.utils import (
    console,
    ensure_venv_exists,
    get_activate_command,
    is_windows,
    print_banner,
)


def run_command() -> None:
    """Print the correct venv activation command for the current platform."""
    print_banner("activate", "Smart cross-platform venv activator")

    ensure_venv_exists()

    cmd = get_activate_command()

    console.print()
    if is_windows():
        console.print("  [yellow]→[/yellow] Run this in PowerShell:")
        console.print(f"    [bold white]{cmd}[/bold white]")
        console.print()
        console.print("  [dim]Or in CMD:[/dim]")
        console.print(r"    [dim].venv\Scripts\activate.bat[/dim]")
    else:
        console.print("  [yellow]→[/yellow] Run this in your terminal:")
        console.print(f"    [bold white]{cmd}[/bold white]")
        console.print()
        console.print("  [dim]Or use eval:[/dim]")
        console.print("    [dim]eval $(stup activate)[/dim]")
    console.print()
