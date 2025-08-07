from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.generate_fake_data import generate_sales_data as sales

default_args = {
    'owner': 'CamilaJaviera',
    'start_date': datetime(2025, 8, 6),
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    dag_id='dbt_postgres_setup',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Pipeline'
) as dag:

    task_sales = PythonOperator(
        task_id='generate_sales_data',
        python_callable=sales,
    )

    task_sales 
