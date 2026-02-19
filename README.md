# Pradeep Jewellers – Gold Rate Card

Fetches live gold/silver rates from All India Bullion and generates a daily rate card image.

## Image URL (GitHub raw)

After the workflow runs and commits the image, you can use:

```
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/gold_rate_card.png
```

Replace `YOUR_USERNAME` and `YOUR_REPO` with your GitHub username and repository name. The image is updated every weekday at 11:00 AM IST (Monday–Saturday).

## Local setup

```bash
pip install -r requirements.txt
playwright install chromium
python generate_rate_image.py
```
