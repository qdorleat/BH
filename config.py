from pathlib import Path

BASE_DIR = Path(__file__).parent

DEFAULT_EXPORT_DIR = BASE_DIR / "exports"
HISTORY_FILE = BASE_DIR / "history" / "send_history.csv"

DEFAULT_EXPORT_DIR.mkdir(exist_ok=True)
HISTORY_FILE.parent.mkdir(exist_ok=True)
