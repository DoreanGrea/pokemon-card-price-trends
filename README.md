# Pokémon Card Price Trends

Historical price analysis for Pokémon cards across the last 5 years with per-card charts and 1–2 year projections.

## Data Sources (manual exports)
Please export CSVs for your target cards and save them into:
- `data/pricecharting/`
- `data/tcgplayer/`
- `data/ebay/`

### Expected CSV schemas
We normalize these columns (case-insensitive headers are okay):

| Column           | Type     | Notes |
|------------------|----------|------|
| date             | date     | Sale date (YYYY-MM-DD or locale recognized by pandas) |
| price            | float    | Final sale price (USD) |
| card_name        | string   | e.g., "Umbreon VMAX (Alt Art) #215/203" |
| set_name         | string   | e.g., "Evolving Skies" |
| grade            | string   | e.g., "PSA 10", "BGS 9.5", "Raw" |
| source           | string   | "pricecharting", "tcgplayer", "ebay" |
| listing_type     | string   | "auction", "buy_it_now" (if known) |
| condition        | string   | Raw condition if available (e.g., "Near Mint") |
| notes            | string   | Optional; e.g., link id, auction id |

> If your CSVs use different headers, the merge script tries to auto-map common variants (e.g., `sold_date`, `soldPrice`, `title`, `grade_text`).

## How to run
```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 1) Merge & clean all CSVs -> data/processed/prices.csv/parquet
python scripts/fetch_price_data.py

# 2) Build per-card annual charts (last 5 yrs) -> charts/*.png
python scripts/plot_price_trends.py --years 5

# 3) Generate 1–2 year price projections -> data/processed/predictions.csv
python scripts/predict_prices.py --years_back 5 --years_ahead 2
