import pandas as pd
import os
import glob

def load_latest_generated_file(directory="data/generate", prefix="raw_sales_"):
    files = glob.glob(f"{directory}/{prefix}*.csv")
    latest_file = max(files, key=os.path.getmtime)
    print(f"Loading latest generated file: {latest_file}")
    return latest_file

def test_generate_data():
    try:
        csv_path = load_latest_generated_file()
    except FileNotFoundError:
        print("No CSV to analyze. Skipping validation.")
        return

    csv_path = load_latest_generated_file()
    df = pd.read_csv(csv_path)

    missing_customer = df[df['customer'] == ""]
    invalid_price = df[df['price'] == "not_a_price"]
    missing_date = df[df['sale_date'] == ""]
    invalid_product = df[df['product'] == "UNKNOWN_PRODUCT"]

    summary = pd.DataFrame({
    "issue": ["missing_customer", "invalid_price", "missing_date", "invalid_product"],
    "count": [len(missing_customer), len(invalid_price), len(missing_date), len(invalid_product)]})

    summary.to_csv("data/tests/findings_summary.csv", index=False)
    print("Findings summary saved to data/tests/findings_summary.csv")

test_generate_data()