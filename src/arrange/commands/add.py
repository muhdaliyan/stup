"""arrange add — Thin wrapper over uv add that maintains requirements.txt."""

import typer
from arrange.utils import (
    check_uv,
    ensure_venv_exists,
    print_banner,
    print_done,
    run,
)

def run_command(packages: list[str]) -> None:
    """Add packages using uv and update requirements.txt."""
    print_banner("add", f"Adding packages: {', '.join(packages)}")

    check_uv()
    ensure_venv_exists()

    # Add packages
    pkg_str = " ".join(packages)
    run(f"uv add {pkg_str}")

    # Update requirements.txt for compatibility (clean format)
    run("uv export --format requirements-txt --no-hashes --no-emit-project --output-file requirements.txt --quiet")

    # Post-process to remove all 'via' comments for a super clean look
    req_file = "requirements.txt"
    with open(req_file, "r") as f:
        lines = f.readlines()
    with open(req_file, "w") as f:
        for line in lines:
            if not line.strip().startswith("#"):
                f.write(line)

    print_done()
