# BookDealer

A storefront app that ranks the top 25 books by purchase count in the last 5 days, using live OpenLibrary metadata for each title.

## What it does

- Pulls real book metadata from OpenLibrary
- Saves the scraped book details to `data/purchases.json`
- Filters sales to the last 5 calendar days
- Sums purchases for each title
- Renders the top 25 books in a clean storefront UI

## Regenerate book data

```bash
python3 scrape_books.py
```

## Run locally

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

## Data source

The catalog metadata comes from the live OpenLibrary API, and the purchase counts are generated for a recent 5-day sales window so the app behaves like a real ranking dashboard.
