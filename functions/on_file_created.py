import time
import logging
import fnmatch
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

WATCHED_DIR = "data/raw"

class FileCreatedHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            logging.debug(f"Ignored directory created: {event.src_path}")
            return

        filename = os.path.basename(event.src_path)

        if fnmatch.fnmatch(filename, "*.csv"):
            logging.info(f"📄 New CSV file detected: {filename}")
            logging.info("🚀 Triggering extract step...")
            try:
                result = subprocess.run(
                    ["python", "extract/extract_from_local.py"],
                    check=True,
                    capture_output=True,
                    text=True
                )
                logging.info(f"✅ Extract script output:\n{result.stdout}")
            except subprocess.CalledProcessError as e:
                logging.error(f"❌ Error running extract script:\n{e.stderr}")
        else:
            logging.debug(f"Ignored file: {filename}")

if __name__ == "__main__":
    if not os.path.exists(WATCHED_DIR):
        logging.error(f"❌ Watched directory does not exist: {WATCHED_DIR}")
        exit(1)

    logging.info(f"👀 Watching directory: {WATCHED_DIR} for any new .csv files")
    event_handler = FileCreatedHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCHED_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("🛑 Stopping file watcher...")
        observer.stop()
    observer.join()
