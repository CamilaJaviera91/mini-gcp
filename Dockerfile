FROM apache/airflow:2.9.0-python3.11 AS default

USER root
RUN apt-get update && apt-get install -y build-essential git

USER airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
