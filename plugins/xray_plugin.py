import subprocess
import json
from rich.console import Console

console = Console()

def run_xray(target: str, flags: list):
    try:
        cmd = ["xray", "webscan", "--basic-crawler", target, "--json-output", "output.json"] + flags
        console.print(f"[cyan]Menjalankan:[/cyan] {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

        with open("output.json", "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        console.print("[red]Xray tidak ditemukan di PATH. Menjalankan mode mock.[/red]")
        return {
            "findings": [
                {"id": "F-0001", "vuln_type": "sql_injection", "severity": "high", "location": "/login"}
            ]
        }
