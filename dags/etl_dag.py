from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.generate_fake_data import generate_sales_data as sales
from export.export_to_postgres import export_duckdb_to_postgres as postgres
from initial_validation.initial_validation import validate_sales_data as validate

default_args = {
    'owner': 'CamilaJaviera',
    'start_date': datetime(2025, 8, 6),
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    dag_id='Mini_GCP',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Pipeline'
) as dag:

    sales_task = PythonOperator(
        task_id='generate_sales_data',
        python_callable=sales,
    )

    postgres_task = PythonOperator(
        task_id='export_duckdb_to_postgres',
        python_callable=postgres,
    )

    validate_task = PythonOperator(
        task_id="validate_sales_data",
        python_callable=validate
    )

    sales_task >> postgres_task >> validate_task
