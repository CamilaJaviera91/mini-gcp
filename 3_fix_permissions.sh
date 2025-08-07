#!/bin/bash

set -e

PROJECT_ROOT=$(pwd)
FOLDERS=("dags" "data" "export" "extract" "functions" "initial_validation" "load" "scripts" "transform" "validate")

# UID and GID you want to use (airflow user inside the container)
TARGET_UID=50000
TARGET_GID=0   # same as the root group that airflow has

echo "Fixing permissions in the project folders for UID:${TARGET_UID}, GID:${TARGET_GID}..."

for folder in "${FOLDERS[@]}"; do
    if [ -d "$PROJECT_ROOT/$folder" ]; then
        echo " - Adjusting permissions and owner in $folder ..."
        # Change owner to UID 50000 and GID 0
        sudo chown -R ${TARGET_UID}:${TARGET_GID} "$PROJECT_ROOT/$folder"
        # Permissions so that the owner has read/write and group/others have read and execute on folders
        sudo find "$PROJECT_ROOT/$folder" -type d -exec chmod 755 {} \;
        sudo find "$PROJECT_ROOT/$folder" -type f -exec chmod 644 {} \;
    else
        echo " - Folder $folder not found, skipping."
    fi
done

echo "✅ Permissions successfully fixed for the airflow user."

# 1. Make sure to give it permissions: chmod +x 3_fix_permissions.sh
# 2. Run: ./3_fix_permissions.sh
