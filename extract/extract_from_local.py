# extract_from_local.py
import os
import shutil
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SOURCE_DIR = "data/raw"
DEST_DIR = "data/extract"
FILENAME_PREFIX = "raw_sales_"
COPY_PREFIX = "copy_raw_sales_"

def main():
    os.makedirs(DEST_DIR, exist_ok=True)

    files = sorted([f for f in os.listdir(SOURCE_DIR) if f.startswith(FILENAME_PREFIX)], reverse=True)
    if not files:
        logging.error("No raw sales file found.")
        return

    latest_file = files[0]
    file_number = latest_file.replace(FILENAME_PREFIX, "").replace(".csv", "")
    src_path = os.path.join(SOURCE_DIR, latest_file)
    dest_path = os.path.join(DEST_DIR, f"{COPY_PREFIX}{file_number}.csv")

    shutil.copy2(src_path, dest_path)
    logging.info(f"Copied {src_path} to {dest_path}")

if __name__ == "__main__":
    main()
