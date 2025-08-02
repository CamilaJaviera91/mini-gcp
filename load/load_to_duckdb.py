import duckdb
import os
import glob

DUCKDB_DIR = "data/warehouse"
os.makedirs(DUCKDB_DIR, exist_ok=True)

def main():
    db_path = os.path.join(DUCKDB_DIR, "sales.duckdb")
    con = duckdb.connect(db_path)

    con.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER,
            customer VARCHAR,
            product VARCHAR,
            price DOUBLE,
            sale_date DATE
        )
    """)

    csv_files = sorted(glob.glob("data/processed/clean_sales_*.csv"))

    if not csv_files:
        print("❌ No hay archivos clean_sales_*.csv en data/processed/")
        return

    latest_file = csv_files[-1]

    con.execute(f"""
        INSERT INTO sales
        SELECT * FROM read_csv_auto('{latest_file}', header=True)
    """)
    print(f"✅ Último archivo cargado: {latest_file}")

    con.close()

if __name__ == "__main__":
    main()
