import duckdb
import pandas as pd
import json
import os

con = duckdb.connect("data/warehouse/sales.duckdb")

df = con.execute("SELECT * FROM sales").fetchdf()

def validate_data(df: pd.DataFrame):
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

    return results

report = validate_data(df)

print("🔍 Validation Report:")
for k, v in report.items():
    print(f"{k}: {v}")

os.makedirs("data/validation", exist_ok=True)

with open("data/validation/validation_report.json", "w") as f:
    json.dump(report, f, indent=4)

pd.DataFrame([report]).to_csv("data/validation/validation_report.csv", index=False)

print("✅ Report saved to:")
print(" - data/validation//validation_report.json")
print(" - data/validation/validation_report.csv")
