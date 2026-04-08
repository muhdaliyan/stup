"""stup scraper — Web scraping pipeline with Playwright & BeautifulSoup."""

from app.utils import (
    check_uv,
    create_dirs,
    ensure_venv_exists,
    print_banner,
    print_done,
    run,
    write_file,
)

# ── Templates ────────────────────────────────────────────────────────

SPIDER_PY = '''\
"""Web spider — fetches pages using Playwright."""

import asyncio
from playwright.async_api import async_playwright


async def scrape(url: str) -> str:
    """Scrape a URL and return the HTML content."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(url, wait_until="networkidle")
        content = await page.content()

        await browser.close()
        return content


async def scrape_multiple(urls: list[str]) -> list[str]:
    """Scrape multiple URLs concurrently."""
    tasks = [scrape(url) for url in urls]
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    url = "https://example.com"
    html = asyncio.run(scrape(url))
    print(f"Scraped {len(html)} characters from {url}")
'''

PIPELINE_PY = '''\
"""Data pipeline — parse HTML and extract structured data."""

import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path


def parse_html(html: str) -> list[dict]:
    """Parse HTML and extract data.

    TODO: Customize selectors for your target site.
    """
    soup = BeautifulSoup(html, "html.parser")

    data = []
    for item in soup.select("article, .item, .listing"):
        record = {
            "title": item.select_one("h1, h2, h3, .title"),
            "description": item.select_one("p, .description"),
            "link": item.select_one("a"),
        }
        data.append({
            "title": record["title"].get_text(strip=True) if record["title"] else "",
            "description": record["description"].get_text(strip=True) if record["description"] else "",
            "link": record["link"]["href"] if record["link"] else "",
        })

    return data


def save_to_csv(data: list[dict], filename: str = "data/raw/scraped.csv") -> None:
    """Save parsed data to CSV."""
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} records to {filename}")


def clean_data(input_path: str = "data/raw/scraped.csv", output_path: str = "data/cleaned/cleaned.csv") -> None:
    """Clean and process scraped data."""
    df = pd.read_csv(input_path)

    # Drop duplicates
    df = df.drop_duplicates()

    # Drop empty rows
    df = df.dropna(subset=["title"])

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data: {len(df)} records saved to {output_path}")


if __name__ == "__main__":
    # Example usage
    sample_html = "<html><body><article><h2>Test</h2><p>Description</p></article></body></html>"
    data = parse_html(sample_html)
    save_to_csv(data)
    clean_data()
'''

SCHEDULER_PY = '''\
"""Scheduler — run scraping jobs on a schedule."""

import schedule
import time
import asyncio
from spider import scrape
from pipeline import parse_html, save_to_csv


def job():
    """Run a scraping job."""
    print("Running scheduled scrape...")
    html = asyncio.run(scrape("https://example.com"))
    data = parse_html(html)
    save_to_csv(data)
    print(f"Scraped {len(data)} records")


# Run every hour
schedule.every(1).hour.do(job)

if __name__ == "__main__":
    print("Scheduler started. Press Ctrl+C to stop.")
    job()  # Run once immediately
    while True:
        schedule.run_pending()
        time.sleep(60)
'''


def run_command() -> None:
    """Scaffold a web scraping project."""
    print_banner("scraper", "Web scraping pipeline with Playwright & BeautifulSoup")

    check_uv()
    ensure_venv_exists()

    # Install scraping dependencies
    run("uv add playwright beautifulsoup4 pandas schedule")

    # Install Playwright browsers
    run("uv run playwright install chromium")

    # Create directory structure
    create_dirs("data/raw", "data/cleaned")

    # Create files
    write_file("spider.py", SPIDER_PY)
    write_file("pipeline.py", PIPELINE_PY)
    write_file("scheduler.py", SCHEDULER_PY)
    write_file("data/raw/.gitkeep", "")
    write_file("data/cleaned/.gitkeep", "")

    print_done()
