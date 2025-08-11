import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

IN_PATH = Path("data/processed/prices.csv")
OUT_DIR = Path("charts")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def plot_card(df, card_name, set_name, grade, years_back=5):
    sub = df[(df.card_name == card_name) & (df.set_name == set_name) & (df.grade == grade)].copy()
    if sub.empty:
        return
    max_year = sub["year"].max()
    min_year = max_year - years_back + 1
    sub = sub[(sub["year"] >= min_year) & (sub["year"] <= max_year)]
    annual = sub.groupby("year")["price"].median().reset_index()

    plt.figure()
    plt.plot(annual["year"], annual["price"], marker="o")
    plt.title(f"{card_name} ({set_name}) — {grade}\nMedian Auction Price by Year")
    plt.xlabel("Year")
    plt.ylabel("Median Price (USD)")
    plt.grid(True)

    slug = f"{sub['card_slug'].iloc[0]}_{sub['grade_slug'].iloc[0]}_annual_trend.png"
    out = OUT_DIR / slug
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved chart -> {out}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", type=int, default=5)
    args = ap.parse_args()

    df = pd.read_csv(IN_PATH, parse_dates=["date"])
    for (card, set_name, grade), group in df.groupby(["card_name","set_name","grade"]):
        plot_card(df, card, set_name, grade, years_back=args.years)

if __name__ == "__main__":
    main()
