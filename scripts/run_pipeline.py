import subprocess
import time

watcher_process = subprocess.Popen(["python", "functions/on_file_created.py"])

time.sleep(2)

subprocess.run(["python", "scripts/generate_fake_data.py"])

time.sleep(2)

subprocess.run(["python", "transform/transform_data_beam.py"])

time.sleep(2)

subprocess.run(["python", "load/load_to_duckdb.py"])

time.sleep(2)

subprocess.run(["python", "export/export_to_postgres.py"])

try:
    print("Pipeline running. Press Ctrl+C to stop.")
    watcher_process.wait()
except KeyboardInterrupt:
    print("Stopping watcher...")
    watcher_process.terminate()
