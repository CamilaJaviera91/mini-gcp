import os
import shutil
import logging
import time
import warnings

def filter_collation_warning(message, category, filename, lineno, file=None, line=None):
    return "collation" not in str(message)

warnings.showwarning = filter_collation_warning

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SOURCE_DIR = "data/raw"
DEST_DIR = "data/extract"
FILENAME_PREFIX = "raw_sales_"
COPY_PREFIX = "copy_raw_sales_"

def wait_for_non_empty_file(path, timeout=5, check_interval=0.5):
    """
    Waits until the file at 'path' has more than one line (i.e., header + data).
    Returns True if the file is ready, False if it times out.
    """
    start = time.time()
    while time.time() - start < timeout:
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if len(lines) > 1:
                    return True
        except Exception:
            pass
        time.sleep(check_interval)
    return False

def extract_from_local():
    os.makedirs(DEST_DIR, exist_ok=True)

    files = sorted(
        [f for f in os.listdir(SOURCE_DIR) if f.startswith(FILENAME_PREFIX) and f.endswith(".csv")],
        reverse=True
    )

    if not files:
        logging.error("❌ No raw sales .csv files found.")
        return

    latest_file = files[0]
    file_number = latest_file[len(FILENAME_PREFIX):-4]
    src_path = os.path.join(SOURCE_DIR, latest_file)
    dest_path = os.path.join(DEST_DIR, f"{COPY_PREFIX}{file_number}.csv")

    if not os.path.exists(src_path):
        logging.error(f"❌ Source file not found: {src_path}")
        return

    if not wait_for_non_empty_file(src_path):
        logging.error(f"⏳ Timeout: File is still empty or incomplete: {src_path}")
        return

    try:
        shutil.copy2(src_path, dest_path)
        logging.info(f"✅ Copied {src_path} to {dest_path}")
    except Exception as e:
        logging.error(f"🚨 Error copying file: {e}")

if __name__ == "__main__":
    extract_from_local()
