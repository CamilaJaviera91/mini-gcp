#!/bin/bash
echo "🧹 Limpiando entorno completo..."
docker compose down --volumes --remove-orphans

echo "⏹️ Deteniendo servicios..."
docker volume prune -f
docker container prune

echo "🔧 Construyendo imágenes..."
docker build --target default .

echo "▶️ Levantando servicios..."
docker compose up -d

echo "Servicios levantados"
docker ps

# 1. Asegúrate de darles permisos: chmod +x 2_reset_docker.sh
# 2. Ejecuta: ./2_reset_docker.sh