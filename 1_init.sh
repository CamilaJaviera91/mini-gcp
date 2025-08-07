#!/bin/bash
echo "🚀 Inicializando Airflow..."
docker compose run --rm airflow-init

# 1. Asegúrate de darles permisos: chmod +x 1_init.sh
# 2. Ejecuta: ./1_init.sh