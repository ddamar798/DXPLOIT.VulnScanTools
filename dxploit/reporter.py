import json
import os
from datetime import datetime

def save_report(report_data: dict, target: str):
    os.makedirs("reports", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/{ts}_{target.replace(':','_').replace('/','_')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
    return filename
