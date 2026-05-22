from datetime import datetime

def generate_filename(prefix="rapport"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.xlsx"
