"""
Fetch live gold/silver rates and generate a 1080x1080 image from gold_rate_card.html.
Uses Playwright for headless browser rendering.
"""

import sys
from pathlib import Path
from typing import Optional

from pradeep_jewellers_rates import scrape_rates, update_rate_card


def generate_image(output_path: Optional[Path] = None) -> bool:
    """Fetch rates, update HTML, and render to PNG. Returns True on success."""
    script_dir = Path(__file__).resolve().parent
    output_path = output_path or (script_dir / "gold_rate_card.png")
    html_path = script_dir / "gold_rate_card.html"

    if not html_path.exists():
        print("Error: gold_rate_card.html not found.")
        return False

    print("Fetching live rates...")
    gold_22k_10g, silver_1kg = scrape_rates()
    if gold_22k_10g is None or silver_1kg is None:
        print("Error: Could not extract rates.")
        return False

    gold_1g = gold_22k_10g / 10
    silver_100g = silver_1kg / 10
    update_rate_card(gold_1g, silver_100g, script_dir)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Error: pip install playwright && playwright install chromium")
        return False

    file_url = html_path.as_uri()
    print("Rendering image...")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=1)
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(500)
        page.locator(".rate-card").first.screenshot(path=str(output_path), type="png")
        browser.close()

    print(f"Saved: {output_path}")
    return True


if __name__ == "__main__":
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    sys.exit(0 if generate_image(output) else 1)
