import csv
from datetime import datetime

from config import HISTORY_FILE

HEADER = [
    "timestamp",
    "recipient",
    "subject",
    "file_path"
]

def initialize_history():
    if not HISTORY_FILE.exists():
        with open(HISTORY_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)

def add_history_entry(recipient, subject, file_path):
    initialize_history()

    with open(HISTORY_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            datetime.now().isoformat(),
            recipient,
            subject,
            str(file_path)
        ])
