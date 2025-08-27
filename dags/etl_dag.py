from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
from airflow.utils.trigger_rule import TriggerRule
import sys

sys.path.append("/opt/airflow")

from scripts.generate_fake_data import generate_fake_data as generate
from scripts.test_generate_fake_data import test_generate_data as test
from extract.extract_from_local import extract_from_local as extract
from initial_validation.initial_validation import initial_validation as ivalidation
from transform.transform_data_beam import transform_data_beam as transform
from load.load_to_duckdb import load_to_duckdb as load
from export.export_to_postgres import export_to_postgres as exportpg
from final_validation.final_validation import final_validation as fvalidation
from export.export_to_bigquery import export_to_bigquery as exportbq
from export.export_to_sheets import export_to_sheets as exportsh
from log_metadata.log_metadata import log_duckdb_metadata as metadata

default_args = {
    'owner': 'CamilaJaviera',
    'start_date': datetime(2025, 8, 6),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email': ['your_email@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'execution_timeout': timedelta(hours=1),
    'sla': timedelta(hours=2),
    'catchup': False,
    'provide_context': True,
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
        python_callable=generate
    )

    test_task = PythonOperator(
        task_id='test_generate_data',
        python_callable=test,
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    extract_task = PythonOperator(
        task_id='extract_from_local',
        python_callable=extract,
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    first_validate_task = PythonOperator(
        task_id="initial_validation",
        python_callable=ivalidation,
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    transform_task = PythonOperator(
        task_id="transform_data_beam",
        python_callable=transform,
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    load_task = PythonOperator(
        task_id="load_to_duckdb",
        python_callable=load,
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    log_duckdb_task = PythonOperator(
        task_id="log_duckdb_metadata",
        python_callable=metadata,
        op_kwargs={
            "db_path": "/opt/airflow/data/load/sales.duckdb",
            "run_id": "{{ run_id }}",
            "task_id": "load_to_duckdb",
            "source_file": "load/sales.duckdb.parquet"
        },
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    exportpg_task = PythonOperator(
        task_id='export_to_postgres',
        python_callable=exportpg,
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    second_validate_task = PythonOperator(
        task_id="final_validation",
        python_callable=fvalidation,
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    exportbq_task = PythonOperator(
        task_id='export_to_bigquery',
        python_callable=exportbq,
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    exportsh_task = PythonOperator(
        task_id='export_to_sheets',
        python_callable=exportsh,
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    generate_task >> test_task >> extract_task >> first_validate_task >> transform_task >> load_task >> log_duckdb_task
    log_duckdb_task >> exportpg_task >> second_validate_task >> exportbq_task >> exportsh_task
