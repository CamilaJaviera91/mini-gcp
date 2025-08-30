from pathlib import Path
import pandas as pd
from scripts.generate_fake_data import generate_fake_data

def load_latest_generated_file(directory="data/generate", prefix="raw_sales_"):
    directory_path = Path(directory)
    directory_path.mkdir(parents=True, exist_ok=True)

    files = list(directory_path.glob(f"{prefix}*.csv"))

    if not files:
        print(f"No CSV found in {directory}, generating a small CSV...")
        generate_fake_data(output_dir=directory, prefix=prefix, num_records=10, num_errors=2)
        files = list(directory_path.glob(f"{prefix}*.csv"))

    if not files:
        raise FileNotFoundError(f"No CSV found in {directory} even after generating one.")

    return max(files, key=lambda f: f.stat().st_mtime)

def test_generate_data(output_dir="data/tests", prefix="test_generate_"):
    csv_path = load_latest_generated_file()
    df = pd.read_csv(csv_path)

    required_cols = ["customer", "product", "price", "sale_date"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    existing_files = [f for f in output_dir_path.glob(f"{prefix}*.csv")]
    numbers = [int(f.stem.replace(prefix, "")) for f in existing_files if f.stem.replace(prefix, "").isdigit()]
    file_number = max(numbers) + 1 if numbers else 1

    output_file = output_dir_path / f"{prefix}{file_number}.csv"

    missing_customer = df['customer'].isna() | (df['customer'].astype(str).str.strip() == "")
    missing_date = df['sale_date'].isna() | (df['sale_date'].astype(str).str.strip() == "")
    invalid_product = df['product'] == "UNKNOWN_PRODUCT"
    invalid_price = df['price'] == "not_a_price"

    summary = pd.DataFrame({
        "issue": ["missing_customer", "invalid_product", "invalid_price", "missing_date"],
        "count": [missing_customer.sum(), invalid_product.sum(), invalid_price.sum(), missing_date.sum()]
    })

    summary.to_csv(output_file, index=False)
    print(f"Findings summary saved to {output_file}")

if __name__ == "__main__":
    try:
        test_generate_data()
    except Exception as e:
        print(f"Error: {e}")
