# Pradeep Jewellers – Gold Rate Card

Fetches live gold/silver rates and generates a daily rate card image.

## Local setup

```bash
pip install -r requirements.txt
playwright install chromium
python generate_rate_image.py
```

The image is saved as `gold_rate_card.png`.

## Schedule daily (Windows Task Scheduler)

1. Create Basic Task → Daily at 11:00 AM
2. Action: Start a program → `python` with argument path to `generate_rate_image.py`
3. Start in: your project folder

## Image URL (GitHub)

If you push to GitHub and use the workflow, the image is available at:

```
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/gold_rate_card.png
```
