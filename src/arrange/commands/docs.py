"""arrange docs — Add MkDocs + Material theme to any project."""

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

MKDOCS_YML = '''\
site_name: My Project Documentation
site_description: Auto-generated documentation
site_url: https://example.com

theme:
  name: material
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.sections
    - navigation.expand
    - search.suggest
    - search.highlight
    - content.code.copy
    - content.tabs.link

plugins:
  - search

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - admonition
  - pymdownx.details
  - attr_list
  - md_in_html
  - toc:
      permalink: true

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - API Reference: api-reference.md
'''

INDEX_MD = '''\
# Welcome

Welcome to the project documentation.

## Quick Start

```bash
# Install dependencies
pip install -e .

# Run the project
python main.py
```

## Features

- Feature 1
- Feature 2
- Feature 3

## Contributing

See the [Getting Started](getting-started.md) guide.
'''

GETTING_STARTED_MD = '''\
# Getting Started

## Prerequisites

- Python 3.11+
- uv (recommended)

## Installation

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Configuration

Create a `.env` file with your settings:

```bash
cp .env.example .env
```

## Running

```bash
python main.py
```
'''

API_REFERENCE_MD = '''\
# API Reference

## Overview

Document your API endpoints and modules here.

## Modules

### `main`

Main entry point for the application.

### `utils`

Utility functions and helpers.
'''


def run_command() -> None:
    """Add MkDocs + Material theme to the current project."""
    print_banner("docs", "MkDocs + Material theme documentation")

    check_uv()
    ensure_venv_exists()

    # Install MkDocs
    run("uv add mkdocs mkdocs-material")

    # Create docs directory
    create_dirs("docs")

    # Create documentation files
    write_file("mkdocs.yml", MKDOCS_YML)
    write_file("docs/index.md", INDEX_MD)
    write_file("docs/getting-started.md", GETTING_STARTED_MD)
    write_file("docs/api-reference.md", API_REFERENCE_MD)

    print_done()
