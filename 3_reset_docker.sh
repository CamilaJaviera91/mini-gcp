#!/bin/bash
echo "🧹 Cleaning up the entire environment..."
docker compose down --volumes --remove-orphans

echo "⏹️ Stopping services..."
docker volume prune -f
docker container prune

echo "🔧 Building images..."
docker build --target default .

echo "▶️ Starting services..."
docker compose up -d

echo "Services started"
docker ps

# 1. Make sure to give it permissions: chmod +x 2_reset_docker.sh
# 2. Run: ./2_reset_docker.sh
