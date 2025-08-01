import subprocess
import time

watcher_process = subprocess.Popen(["python", "functions/on_file_created.py"])

time.sleep(2)

subprocess.run(["python", "scripts/generate_fake_data.py"])

try:
    print("Pipeline running. Press Ctrl+C to stop.")
    watcher_process.wait()
except KeyboardInterrupt:
    print("Stopping watcher...")
    watcher_process.terminate()
