import duckdb
import pandas as pd
import json
import os

def final_validation():
    con = duckdb.connect("data/load/sales.duckdb")

    df = con.execute("SELECT * FROM sales").fetchdf()

    results = {}
    results["total_rows"] = len(df)
    results["nulls_per_column"] = df.isnull().sum().to_dict()
    results["invalid_prices"] = df[df["price"] <= 0].shape[0]

    try:
        df["sale_date"] = pd.to_datetime(df["sale_date"])
        min_date = df["sale_date"].min()
        max_date = df["sale_date"].max()

        results["min_date"] = min_date.strftime("%Y-%m-%d") if pd.notnull(min_date) else None
        results["max_date"] = max_date.strftime("%Y-%m-%d") if pd.notnull(max_date) else None
    except Exception as e:
        results["date_parsing_error"] = str(e)

    os.makedirs("data/fvalidation", exist_ok=True)
    with open("data/fvalidation/validation_report.json", "w") as f:
        json.dump(results, f, indent=4)
    pd.DataFrame([results]).to_csv("data/fvalidation/validation_report.csv", index=False)

    print("✅ Validation report saved!")

if __name__ == "__main__":
    final_validation()
