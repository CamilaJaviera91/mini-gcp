import os
import pandas as pd
from sqlalchemy import create_engine, inspect
from google.cloud import bigquery

def export_to_bigquery():

    PG_HOST = os.getenv("POSTGRES_HOST")
    PG_PORT = os.getenv("POSTGRES_PORT")
    PG_DB = os.getenv("POSTGRES_DB")
    PG_USER = os.getenv("POSTGRES_USER")
    PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    PG_SCHEMA = os.getenv("POSTGRES_SCHEMA")


    postgres_url = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    engine = create_engine(postgres_url)

    BQ_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS_PATH")
    BQ_PROJECT = os.getenv("BQ_PROJECT_ID")
    BQ_DATASET = os.getenv("BQ_DATASET")

    if not BQ_PROJECT or not BQ_DATASET:
        raise ValueError("Missing BQ_PROJECT_ID or BQ_DATASET environment variables.")

    if BQ_CREDENTIALS:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = BQ_CREDENTIALS

    client = bigquery.Client(project=BQ_PROJECT)
    dataset_ref = bigquery.Dataset(f"{BQ_PROJECT}.{BQ_DATASET}")
    try:
        client.get_dataset(dataset_ref) # type: ignore
    except Exception:
        print(f"📁 Dataset {BQ_DATASET} not found. Creating it...")
        client.create_dataset(dataset_ref)
        print(f"✅ Dataset {BQ_DATASET} created.")

    inspector = inspect(engine)
    table_names = inspector.get_table_names(schema=PG_SCHEMA) # type: ignore

    for table in table_names:
        full_table_name = f"{BQ_DATASET}.{table}"
        print(f"📤 Uploading table: {PG_SCHEMA}.{table} ➡️ {full_table_name}")

        df = pd.read_sql_table(table_name=table, con=engine, schema=PG_SCHEMA)
        df.to_gbq(
            destination_table=full_table_name,
            project_id=BQ_PROJECT,
            if_exists="replace"
        )

        print(f"✅ Table '{table}' loaded successfully.")

if __name__ == "__main__":
    export_to_bigquery()