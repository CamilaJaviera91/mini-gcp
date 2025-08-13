import duckdb
import os
import glob

DUCKDB_DIR = "data/warehouse"
os.makedirs(DUCKDB_DIR, exist_ok=True)

def load_to_duckdb():
    db_path = os.path.join(DUCKDB_DIR, "sales.duckdb")
    con = duckdb.connect(db_path)

    csv_files = sorted(glob.glob("data/processed/clean_sales_*.csv"))
    if not csv_files:
        print("❌ No hay archivos clean_sales_*.csv en data/processed/")
        return

    latest_file = csv_files[-1]

    con.execute(f"""
        CREATE OR REPLACE TABLE sales AS
        SELECT * FROM read_csv_auto('{latest_file}', header=True)
    """)

    print(f"✅ Último archivo cargado: {latest_file}")

    df = con.execute("SELECT * FROM sales").df()
    
    print(df.head())

    con.close()

if __name__ == "__main__":
    load_to_duckdb()
