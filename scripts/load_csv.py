import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("retail.db")
CSV_PATH = Path("data/retail_sales.csv")

EXPECTED_COLS = [
    "transactions_id","sale_date","sale_time","customer_id","gender","age",
    "category","quantity","price_per_unit","cogs","total_sale"
]

def main():
    df = pd.read_csv(CSV_PATH)

    # Clean column names (handles extra spaces)
    df.columns = [c.strip() for c in df.columns]

    # If columns don't match exactly, show what we got (helps debugging)
    # print("CSV columns:", df.columns.tolist())

    # Keep only expected columns if CSV has extras
    if set(EXPECTED_COLS).issubset(set(df.columns)):
        df = df[EXPECTED_COLS]
    else:
        # If the CSV headers differ slightly, fail loudly so we can map them correctly.
        missing = [c for c in EXPECTED_COLS if c not in df.columns]
        raise ValueError(f"CSV missing expected columns: {missing}. Found: {df.columns.tolist()}")

    # Normalize types (don’t drop everything)
    numeric_cols = ["transactions_id","customer_id","age","quantity","price_per_unit","cogs","total_sale"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Normalize date/time as strings
    df["sale_date"] = df["sale_date"].astype(str).str.strip()
    df["sale_time"] = df["sale_time"].astype(str).str.strip()

    # Drop only rows missing essential fields (not every missing value)
    df = df.dropna(subset=["transactions_id", "sale_date", "sale_time", "customer_id", "category", "total_sale"])

    # Convert IDs to int after dropping NaNs
    df["transactions_id"] = df["transactions_id"].astype(int)
    df["customer_id"] = df["customer_id"].astype(int)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM retail_sales;")  # reload cleanly
        df.to_sql("retail_sales", conn, if_exists="append", index=False)

    print(f"Loaded {len(df)} rows into retail_sales")

if __name__ == "__main__":
    main()
