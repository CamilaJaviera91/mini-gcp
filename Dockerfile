# Dockerfile
FROM apache/airflow:2.9.1-python3.10 AS default

USER root
RUN apt-get update && apt-get install -y build-essential libpq-dev python3-dev

USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt
