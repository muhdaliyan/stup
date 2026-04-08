"""arrange cli — PyPI-ready CLI package with Typer + Rich."""

import os

from arrange.utils import (
    check_uv,
    create_dirs,
    ensure_venv_exists,
    print_banner,
    print_done,
    run,
    write_file,
)

# ── Templates ────────────────────────────────────────────────────────


def _get_templates(project_name: str) -> dict[str, str]:
    """Return template files with project name substituted."""
    return {
        "init": f'''\
"""{project_name} — A CLI tool built with Typer + Rich."""

__version__ = "0.1.0"
''',
        "main": f'''\
"""Entry point for {project_name} CLI."""

import typer
from rich.console import Console
from {project_name} import __version__
from {project_name}.commands import hello

console = Console()

app = typer.Typer(
    name="{project_name}",
    help="🚀 {project_name} CLI",
    add_completion=False,
    rich_markup_mode="rich",
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"[bold cyan]{project_name}[/bold cyan] v{{__version__}}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-v", help="Show version.", callback=_version_callback, is_eager=True
    ),
) -> None:
    pass


@app.command()
def greet(name: str = typer.Argument("World", help="Name to greet.")) -> None:
    """Say hello to someone."""
    hello.greet(name)


if __name__ == "__main__":
    app()
''',
        "hello": '''\
"""Hello command implementation."""

from rich.console import Console

console = Console()


def greet(name: str) -> None:
    """Print a greeting."""
    console.print(f"[bold green]Hello, {name}![/bold green] 👋")
''',
        "commands_init": '''\
"""CLI commands package."""
''',
    }


def run_command() -> None:
    """Scaffold a PyPI-ready CLI package."""
    print_banner("cli", "PyPI-ready CLI package with Typer + Rich")

    check_uv()
    ensure_venv_exists()

    # Use current directory name as project name
    project_name = os.path.basename(os.getcwd()).replace("-", "_").replace(" ", "_").lower()

    # Install CLI dependencies
    run("uv add typer rich")

    templates = _get_templates(project_name)

    # Create package structure
    create_dirs(f"src/{project_name}/commands")

    write_file(f"src/{project_name}/__init__.py", templates["init"])
    write_file(f"src/{project_name}/__main__.py", templates["main"])
    write_file(f"src/{project_name}/commands/__init__.py", templates["commands_init"])
    write_file(f"src/{project_name}/commands/hello.py", templates["hello"])

    # Create README
    readme = f"""\
# {project_name}

A CLI tool built with [Typer](https://typer.tiangolo.com/) + [Rich](https://rich.readthedocs.io/).

## Installation

```bash
pip install {project_name}
```

## Usage

```bash
{project_name} --help
{project_name} greet "World"
```

## Development

```bash
uv pip install -e .
```
"""
    write_file("README.md", readme)

    print_done()
