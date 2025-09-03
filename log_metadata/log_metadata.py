import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import warnings
import duckdb

warnings.filterwarnings("ignore", message=".*collation.*")

load_dotenv()

PG_HOST = os.getenv("POSTGRES_HOST")
PG_PORT = os.getenv("POSTGRES_PORT")
PG_DB = os.getenv("POSTGRES_DB")
PG_USER = os.getenv("POSTGRES_USER")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
PG_LOG_SCHEMA = os.getenv("POSTGRES_LOG_SCHEMA")

engine = create_engine(
    f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
)

def log_metadata(run_id, task_id, status, row_count=None, source=None, target=None):
    try:
        with engine.begin() as conn:
            conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{PG_LOG_SCHEMA}"'))

            conn.execute(
                text(f"""
                    CREATE TABLE IF NOT EXISTS "{PG_LOG_SCHEMA}".pipeline_metadata (
                        id SERIAL PRIMARY KEY,
                        run_id TEXT,
                        task_id TEXT,
                        status TEXT,
                        row_count INT,
                        source_file TEXT,
                        target_table TEXT,
                        logged_at TIMESTAMP DEFAULT now()
                    )
                """)
            )

            conn.execute(
                text(f"""
                    INSERT INTO "{PG_LOG_SCHEMA}".pipeline_metadata
                    (run_id, task_id, status, row_count, source_file, target_table)
                    VALUES (:run_id, :task_id, :status, :row_count, :source, :target)
                """),
                {
                    "run_id": run_id,
                    "task_id": task_id,
                    "status": status,
                    "row_count": row_count,
                    "source": source,
                    "target": target,
                }
            )

            print(f"✅ Metadata logged for task {task_id} (run_id={run_id})")

    except Exception as e:
        print(f"❌ Failed to log metadata: {e}")
        raise

def log_duckdb_metadata(db_path: str, run_id: str, task_id: str, source_file: str):
    con = duckdb.connect(db_path)
    
    tables = con.execute("SHOW TABLES").fetchall()
    if not tables:
        raise ValueError("No tables found in DuckDB file")
    
    table_name = tables[-1][0]  # tables is a list of tuples: [('table_name',), ...]
    
    row_count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    con.close()
    
    log_metadata(
        run_id=run_id,
        task_id=task_id,
        status="SUCCESS",
        row_count=row_count,
        source=source_file,
        target=f"duckdb.{table_name}"
    )

if __name__ == "__main__":
    log_duckdb_metadata(
        db_path="/opt/airflow/data/load/sales.duckdb",
        run_id="test_run",
        task_id="load_to_duckdb",
        source_file="load/sales.duckdb.parquet"
    )
