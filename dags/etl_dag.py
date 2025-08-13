from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.generate_fake_data import generate_fake_data as generate
from extract.extract_from_local import extract_from_local as extract
from initial_validation.initial_validation import initial_validation as ivalidation
from transform.transform_data_beam import transform_data_beam as transform
from load.load_to_duckdb import load_to_duckdb as load
from export.export_to_postgres import export_to_postgres as export
from final_validation.final_validation import final_validation as fvalidation

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

    generate_task = PythonOperator(
        task_id='generate_fake_data',
        python_callable=generate,
    )

    extract_task = PythonOperator(
        task_id='extract_from_local',
        python_callable=extract,
    )

    first_validate_task = PythonOperator(
        task_id="initial_validation",
        python_callable=ivalidation
    )

    transform_task = PythonOperator(
        task_id="transform_data_beam",
        python_callable=transform
    )

    load_task = PythonOperator(
        task_id="load_to_duckdb",
        python_callable=load
    )

    export_task = PythonOperator(
        task_id='export_duckdb_to_postgres',
        python_callable=export,
    )

    second_validate_task = PythonOperator(
        task_id="final_validation",
        python_callable=fvalidation
    )

    generate_task >> extract_task >> first_validate_task >> transform_task >> load_task >> export_task >> second_validate_task
