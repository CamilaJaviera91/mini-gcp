import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import duckdb

load_dotenv()

PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_SCHEMA = os.getenv("PG_SCHEMA")

def export_duckdb_to_postgres():
    con = duckdb.connect("data/warehouse/sales.duckdb")
    df = con.execute("SELECT * FROM sales").df()
    con.close()

    engine = create_engine(f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}")
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schema
        """), {"schema": PG_SCHEMA})
        if result.fetchone() is None:
            conn.execute(text(f'CREATE SCHEMA "{PG_SCHEMA}"'))
            print(f"🛠️  Schema '{PG_SCHEMA}' created")

        conn.execute(text(f'SET search_path TO "{PG_SCHEMA}"'))

        df.to_sql("sales", con=conn, index=False, if_exists="append", schema=PG_SCHEMA)
        print("✅ Exported DuckDB sales table to PostgreSQL")

if __name__ == "__main__":
    export_duckdb_to_postgres()
