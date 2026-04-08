"""arrange test — Scaffold a full pytest suite with coverage."""

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

CONFTEST = '''\
"""Shared pytest fixtures."""

import pytest


@pytest.fixture
def sample_data():
    """Provide sample test data."""
    return {
        "name": "Test",
        "value": 42,
        "items": ["a", "b", "c"],
    }


@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary file for testing."""
    file = tmp_path / "test_file.txt"
    file.write_text("test content")
    return file
'''

SAMPLE_TEST = '''\
"""Sample test file — replace with your actual tests."""


def test_example(sample_data):
    """Example test using a fixture."""
    assert sample_data["name"] == "Test"
    assert sample_data["value"] == 42


def test_addition():
    """Basic sanity check."""
    assert 1 + 1 == 2


class TestExample:
    """Example test class."""

    def test_string_upper(self):
        assert "hello".upper() == "HELLO"

    def test_list_length(self, sample_data):
        assert len(sample_data["items"]) == 3
'''

FIXTURES_INIT = '''\
"""Shared test fixtures.

Import fixtures from here to reuse across test modules:

    from fixtures import my_fixture
"""
'''

COVERAGERC = '''\
[run]
source = src
omit =
    tests/*
    */__pycache__/*
    */migrations/*

[report]
show_missing = true
precision = 2
fail_under = 80

[html]
directory = htmlcov
'''

PYTEST_INI = '''\
# pytest configuration is in pyproject.toml
# Run tests with: uv run pytest
# Run with coverage: uv run pytest --cov --cov-report=html
'''


def run_command() -> None:
    """Scaffold a pytest test suite with coverage."""
    print_banner("test", "pytest suite with coverage config")

    check_uv()
    ensure_venv_exists()

    # Install test dependencies
    run("uv add --dev pytest pytest-cov")

    # Create directory structure
    create_dirs("tests", "tests/fixtures")

    # Create files
    write_file("tests/__init__.py", "")
    write_file("tests/conftest.py", CONFTEST)
    write_file("tests/test_example.py", SAMPLE_TEST)
    write_file("tests/fixtures/__init__.py", FIXTURES_INIT)
    write_file(".coveragerc", COVERAGERC)

    print_done()
