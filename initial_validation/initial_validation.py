# validate_data.py
import pandas as pd
import json
import os
import glob
import numpy as np

def initial_validation(input_pattern="data/extract/copy_raw_sales_*.csv",
                        output_dir="data/initial_validation"):
    """
    Validate sales data and save results as JSON and CSV.

    Args:
        input_pattern (str): Glob pattern to find the sales CSV files.
        output_dir (str): Directory to store the validation reports.
    """
    # Find latest file
    csv_files = sorted(glob.glob(input_pattern))
    if not csv_files:
        raise FileNotFoundError(f"❌ No se encontraron archivos con patrón '{input_pattern}'")

    latest_file = csv_files[-1]
    print(f"📄 Initial Validation: {latest_file}")

    # Load data
    df = pd.read_csv(latest_file)

    # Run validation
    report = _validate_data(df)

    # Ensure JSON-serializable values
    serializable_report = _convert_to_serializable(report)

    # Save results
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, "initial_validation.json")
    csv_path = os.path.join(output_dir, "initial_validation.csv")

    with open(json_path, "w") as f:
        json.dump(serializable_report, f, indent=4)

    pd.DataFrame([serializable_report]).to_csv(csv_path, index=False)

    print("✅ Report saved to:")
    print(f" - {json_path}")
    print(f" - {csv_path}")

    return serializable_report  # Can be used in XCom

def _validate_data(df: pd.DataFrame):
    """Perform validation checks on the sales DataFrame."""
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

def _convert_to_serializable(obj):
    """Convert NumPy and non-serializable objects to Python native types."""
    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    elif isinstance(obj, dict):
        return {k: _convert_to_serializable(v) for k, v in obj.items()}
    else:
        return obj
