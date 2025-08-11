# Dockerfile
FROM apache/airflow:2.9.0-python3.11 AS default

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
