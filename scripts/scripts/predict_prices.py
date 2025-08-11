import argparse
from pathlib import Path
import numpy as np
import pandas as pd

IN_PATH = Path("data/processed/prices.csv")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def predict_series(years, values, years_ahead=2):
    x = np.array(years, dtype=float)
    y = np.array(values, dtype=float)
    if len(x) < 2:
        return pd.DataFrame(columns=["year","pred","lo","hi"])
    m, b = np.polyfit(x, y, 1)
    resid = y - (m*x + b)
    sigma = np.std(resid) if len(resid) > 1 else 0.0

    last_year = int(max(years))
    future_years = [last_year + i for i in range(1, years_ahead+1)]
    preds = [(fy, m*fy + b, m*fy + b - 0.84*sigma, m*fy + b + 0.84*sigma) for fy in future_years]
    return pd.DataFrame(preds, columns=["year","pred","lo","hi"])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years_back", type=int, default=5)
    ap.add_argument("--years_ahead", type=int, default=2)
    args = ap.parse_args()

    df = pd.read_csv(IN_PATH, parse_dates=["date"])
    df["year"] = df["date"].dt.year
    out_rows = []
    for (card, set_name, grade), g in df.groupby(["card_name","set_name","grade"]):
        max_year = g["year"].max()
        min_year = max_year - args.years_back + 1
        gg = g[(g["year"] >= min_year) & (g["year"] <= max_year)]
        if gg.empty:
            continue
        annual = gg.groupby("year")["price"].median().reset_index()
        pred = predict_series(annual["year"].tolist(), annual["price"].tolist(), years_ahead=args.years_ahead)
        for _, r in pred.iterrows():
            out_rows.append({
                "card_name": card,
                "set_name": set_name,
                "grade": grade,
                "forecast_year": int(r["year"]),
                "predicted_price": float(r["pred"]),
                "band_lo": float(r["lo"]),
                "band_hi": float(r["hi"]),
                "history_years_used": len(annual)
            })
    out_df = pd.DataFrame(out_rows)
    out_df.to_csv(OUT_DIR / "predictions.csv", index=False)
    print(f"Saved predictions -> {OUT_DIR / 'predictions.csv'}")

if __name__ == "__main__":
    main()
