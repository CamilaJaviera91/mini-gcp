import duckdb
import os
import glob

DUCKDB_DIR = "data/load"
os.makedirs(DUCKDB_DIR, exist_ok=True)

def load_to_duckdb():
    db_path = os.path.join(DUCKDB_DIR, "sales.duckdb")
    con = duckdb.connect(db_path)

    csv_files = sorted(glob.glob("data/transform/clean_sales_*.csv"))
    if not csv_files:
        print("❌ There's no clean_sales_*.csv in data/transform/")
        return

    con.execute("""
        CREATE TABLE IF NOT EXISTS sales AS
        SELECT * FROM read_csv_auto('data/transform/clean_sales_1.csv', header=True)
        LIMIT 0
    """)

    for file in csv_files:
        print(f"📥 Loading {file} into DuckDB...")
        con.execute(f"""
            INSERT INTO sales
            SELECT DISTINCT * FROM read_csv_auto('{file}', header=True)
        """)

    con.execute("""
        CREATE OR REPLACE TABLE sales AS
        SELECT DISTINCT * FROM sales
    """)

    print("✅ All CSVs loaded into DuckDB (deduplicated)")

    df = con.execute("SELECT COUNT(*) as total_rows FROM sales").df()
    print(df)

    con.close()

if __name__ == "__main__":
    load_to_duckdb()
