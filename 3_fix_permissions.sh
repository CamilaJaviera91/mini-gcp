#!/bin/bash

set -e

PROJECT_ROOT=$(pwd)
FOLDERS=("dags" "data" "export" "extract" "functions" "initial_validation" "load" "scripts" "transform" "validate")

# UID y GID que quieres usar (usuario airflow dentro del contenedor)
TARGET_UID=50000
TARGET_GID=0   # como el grupo root que tiene airflow

echo "Corrigiendo permisos en las carpetas del proyecto para UID:${TARGET_UID}, GID:${TARGET_GID}..."

for folder in "${FOLDERS[@]}"; do
    if [ -d "$PROJECT_ROOT/$folder" ]; then
        echo " - Ajustando permisos y propietario en $folder ..."
        # Cambiar propietario a UID 50000 y GID 0
        sudo chown -R ${TARGET_UID}:${TARGET_GID} "$PROJECT_ROOT/$folder"
        # Permisos para que el propietario tenga lectura/escritura y grupo/otros solo lectura y ejecución en carpetas
        sudo find "$PROJECT_ROOT/$folder" -type d -exec chmod 755 {} \;
        sudo find "$PROJECT_ROOT/$folder" -type f -exec chmod 644 {} \;
    else
        echo " - Carpeta $folder no encontrada, se omite."
    fi
done

echo "✅ Permisos corregidos exitosamente para el usuario airflow."
