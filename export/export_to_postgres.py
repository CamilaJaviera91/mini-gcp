import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import duckdb
import pandas as pd

load_dotenv()

PG_HOST = os.getenv("POSTGRES_HOST")
PG_PORT = os.getenv("POSTGRES_PORT")
PG_DB = os.getenv("POSTGRES_DB")
PG_USER = os.getenv("POSTGRES_USER")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
PG_SCHEMA = os.getenv("POSTGRES_SCHEMA")

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

        table_columns = []
        result = conn.execute(text("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_schema = :schema AND table_name = 'sales'
        """), {"schema": PG_SCHEMA})
        table_columns = [row[0] for row in result.fetchall()]

        if not table_columns:
            conn.execute(text(f"""
                CREATE TABLE "{PG_SCHEMA}".sales (
                    id INTEGER,
                    customer VARCHAR,
                    product VARCHAR,
                    price FLOAT,
                    sale_date DATE
                )
            """))
            print("🛠️  Table 'sales' created in schema", PG_SCHEMA)
        
        else:
            df_columns = df.columns.tolist()
            if set(df_columns) != set(table_columns):
                print("❌ Column mismatch:")
                print("DataFrame columns:", df_columns)
                print("Table columns:", table_columns)
                return

        df.to_sql("sales", con=conn, index=False, if_exists="append", schema=PG_SCHEMA)
        print("✅ Exported DuckDB sales table to PostgreSQL")

if __name__ == "__main__":
    export_duckdb_to_postgres()
