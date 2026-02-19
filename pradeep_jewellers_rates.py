"""
Scrape gold and silver rates from All India Bullion for Pradeep Jewellers.
Extracts 22K gold (10g), Retail 999 silver (1kg), and calculates derived prices.
Uses JSON-LD schema data from the page for reliable extraction.
Updates gold_rate_card.html with current rates.
"""

import json
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def scrape_rates():
    url = "https://allindiabullion.com/gold-rate/gujarat/ahmedabad"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    gold_22k_10g = None
    silver_retail_999_1kg = None

    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get("@type") == "Product":
                name = data.get("name", "").lower()
                offers = data.get("offers", [])
                if "gold" in name:
                    for offer in offers:
                        oname = (offer.get("name") or "").lower()
                        if "22k" in oname and "10g" in oname:
                            gold_22k_10g = float(offer.get("price", 0))
                            break
                elif "silver" in name:
                    for offer in offers:
                        oname = (offer.get("name") or "").lower()
                        if "999" in oname and "1kg" in oname and "retail" in oname:
                            silver_retail_999_1kg = float(offer.get("price", 0))
                            break
        except (json.JSONDecodeError, TypeError):
            continue

    return gold_22k_10g, silver_retail_999_1kg


def update_rate_card(gold_1g: float, silver_100g: float, script_dir: Path) -> None:
    """Update gold_rate_card.html with current rates and date."""
    html_path = script_dir / "gold_rate_card.html"
    if not html_path.exists():
        return
    html = html_path.read_text(encoding="utf-8")
    date_str = datetime.now().strftime("%d %b %Y").upper()
    gold_str = f"₹ {gold_1g:,.2f}"
    silver_str = f"₹ {silver_100g:,.2f}"
    html = re.sub(
        r"(Today's Gold Rate \(22KT 1g\)</div>\s*<div class=\"price\">)₹ [\d,]+\.\d+",
        r"\1" + gold_str,
        html,
    )
    html = re.sub(
        r"(Today's Silver Rate \(100g\)</div>\s*<div class=\"price\">)₹ [\d,]+\.\d+",
        r"\1" + silver_str,
        html,
    )
    html = re.sub(r"\d{1,2} [A-Z]{3} \d{4}", date_str, html, count=1)
    html_path.write_text(html, encoding="utf-8")


def main():
    gold_22k_10g, silver_1kg = scrape_rates()
    if gold_22k_10g is None or silver_1kg is None:
        print("Error: Could not extract rates.")
        return
    gold_1g = gold_22k_10g / 10
    silver_100g = silver_1kg / 10
    script_dir = Path(__file__).resolve().parent
    update_rate_card(gold_1g, silver_100g, script_dir)
    print(f"22KT GOLD (1g): Rs. {gold_1g:,.2f}")
    print(f"SILVER (100g): Rs. {silver_100g:,.2f}")


if __name__ == "__main__":
    main()
