#!/bin/bash
echo "🚀 Initializing Airflow..."

DOCKER_BUILDKIT=0 docker compose build airflow-init

docker compose run --rm airflow-init

# 1. Make sure to give it permissions: chmod +x 1_init.sh
# 2. Run: ./1_init.sh
