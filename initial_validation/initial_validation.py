import pandas as pd
import json
import os
import glob
import numpy as np

csv_files = sorted(glob.glob("data/extract/copy_raw_sales_*.csv"))

if not csv_files:
    raise FileNotFoundError("❌ No se encontraron archivos 'copy_raw_sales_*.csv'")

latest_file = csv_files[-1]

print(f"📄 Initial Validation: {latest_file}")

df = pd.read_csv(latest_file)

def validate_data(df: pd.DataFrame):
    results = {}
    results["total_rows"] = len(df)
    results["nulls_per_column"] = df.isnull().sum().to_dict()

    results["missing_customers"] = df["customer"].isnull().sum() + (df["customer"] == "").sum()

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    results["invalid_prices"] = df["price"].isnull().sum() + (df["price"] <= 0).sum()

    df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
    results["invalid_dates"] = df["sale_date"].isnull().sum()

    min_date = df["sale_date"].min()
    max_date = df["sale_date"].max()
    results["min_date"] = min_date.strftime("%Y-%m-%d") if pd.notnull(min_date) else None
    results["max_date"] = max_date.strftime("%Y-%m-%d") if pd.notnull(max_date) else None

    results["invalid_products"] = (df["product"] == "UNKNOWN_PRODUCT").sum()

    results["total_issues"] = (
        results["missing_customers"] +
        results["invalid_prices"] +
        results["invalid_dates"] +
        results["invalid_products"]
    )
    
    return results

def convert_to_serializable(obj):
    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    else:
        return obj

report = validate_data(df)
serializable_report = convert_to_serializable(report)

print("🔍 Validation Report:")
for k, v in serializable_report.items():
    print(f"{k}: {v}")

os.makedirs("data/initial_validation", exist_ok=True)

file_id = os.path.splitext(os.path.basename(latest_file))[0].split("_")[-1]

json_path = f"data/initial_validation/initial_validation.json"
csv_path = f"data/initial_validation/initial_validation.csv"

with open(json_path, "w") as f:
    json.dump(serializable_report, f, indent=4)

pd.DataFrame([serializable_report]).to_csv(csv_path, index=False)

print("✅ Report saved to:")
print(f" - {json_path}")
print(f" - {csv_path}")
