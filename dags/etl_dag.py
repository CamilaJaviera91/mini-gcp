from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.trigger_rule import TriggerRule
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.generate_fake_data import generate_fake_data as generate
from extract.extract_from_local import extract_from_local as extract
from initial_validation.initial_validation import initial_validation as ivalidation
from transform.transform_data_beam import transform_data_beam as transform
from load.load_to_duckdb import load_to_duckdb as load
from export.export_to_postgres import export_to_postgres as exportpg
from final_validation.final_validation import final_validation as fvalidation
from export.export_to_bigquery import export_to_bigquery as exportbq
from export.export_to_sheets import export_to_sheets as exportsh

default_args = {
    'owner': 'CamilaJaviera',                # Person responsible for the DAG/tasks
    'start_date': datetime(2025, 8, 6),      # Date when the DAG should start scheduling
    'depends_on_past': False,                # Task doesn't wait for previous run to succeed
    'retries': 1,                            # Number of retry attempts if a task fails
    'retry_delay': timedelta(minutes=5),     # wait time between retries
    'email': ['your_email@example.com'],     # email for alerts
    'email_on_failure': True,                # send email if task fails
    'email_on_retry': False,                 # send email when task is retried
    'execution_timeout': timedelta(hours=1), # max time a task can run
    'sla': timedelta(hours=2),               # expected time for task completion
    'catchup': False,                        # avoid backfilling old runs
    'provide_context': True,                 # pass context to tasks (older versions)
}

with DAG(
    dag_id='Mini_GCP',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='Pipeline'
) as dag:

    generate_task = PythonOperator(
        task_id='generate_fake_data',
        python_callable=generate,
        doc_md="""Generate synthetic data to initialize the pipeline."""
    )

    extract_task = PythonOperator(
        task_id='extract_from_local',
        python_callable=extract,
        doc_md="""Create a backup copy of the generated data.""",
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    first_validate_task = PythonOperator(
        task_id="initial_validation",
        python_callable=ivalidation,
        doc_md="""Conduct the first validation step for the backup data.""",
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    transform_task = PythonOperator(
        task_id="transform_data_beam",
        python_callable=transform,
        doc_md="""Review the backup data, clean any corrupted records, and generate a new file.""",
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    load_task = PythonOperator(
        task_id="load_to_duckdb",
        python_callable=load,
        doc_md="""Generate a DuckDB database using the cleaned dataset.""",
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    exportpg_task = PythonOperator(
        task_id='export_to_postgres',
        python_callable=exportpg,
        doc_md="""Load the DuckDB data into a PostgreSQL database.""",
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    second_validate_task = PythonOperator(
        task_id="final_validation",
        python_callable=fvalidation,
        doc_md="""Conduct the second and final validation step for the DuckDB data.""",
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    exportbq_task = PythonOperator(
        task_id='export_to_bigquery',
        python_callable=exportbq,
        doc_md="""Load the PostgreSQL database into BigQuery.""",
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    exportsh_task = PythonOperator(
        task_id='export_to_sheets',
        python_callable=exportsh,
        doc_md="""Load the PostgreSQL database into GoogleSheets""",
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    generate_task >> extract_task >> first_validate_task >> transform_task >> load_task >> exportpg_task >> second_validate_task >> exportbq_task >> exportsh_task
