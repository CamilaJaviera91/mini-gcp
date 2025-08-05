import os
import shutil
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SOURCE_DIR = "data/raw"
DEST_DIR = "data/extract"
COPY_PREFIX = "copy_"

def main():
    os.makedirs(DEST_DIR, exist_ok=True)

    csv_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(".csv")]

    if not csv_files:
        logging.error("❌ There's no .csv file in the origin folder.")
        return

    csv_files_full_paths = [os.path.join(SOURCE_DIR, f) for f in csv_files]
    csv_files_sorted = sorted(csv_files_full_paths, key=os.path.getmtime, reverse=True)

    latest_file_path = csv_files_sorted[0]
    latest_file_name = os.path.basename(latest_file_path)
    logging.info(f"✅ Last file found: {latest_file_name}")

    dest_file_name = COPY_PREFIX + latest_file_name.replace(".csv", "") + ".csv"
    dest_path = os.path.join(DEST_DIR, dest_file_name)

    shutil.copy2(latest_file_path, dest_path)
    logging.info(f"📁 Copied file: {dest_path}")

if __name__ == "__main__":
    main()
