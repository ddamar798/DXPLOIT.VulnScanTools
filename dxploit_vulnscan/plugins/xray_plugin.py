"""
Xray plugin wrapper.
- Tries to call xray (binary from config) with flags and produce JSON output file.
- If binary not found, returns mock JSON dict for testing.
"""
from pathlib import Path
import json
import time
from typing import List, Dict, Any
from ..config import load_config
from ..executor import run_command, tool_exists
from ..ui_utils import console

CONF = load_config()

def build_xray_cmd(target: str, flags: List[str], out_json: Path) -> List[str]:
    xray_bin = CONF.get("tools", {}).get("xray_path", "xray")
    cmd = [xray_bin, "webscan", "--url", target, "--json-output", str(out_json)] + flags
    return cmd

def create_mock_output(target: str, out_json: Path) -> Dict[str, Any]:
    sample = {
        "target": target,
        "results": [
            {"type": "sql_injection", "url": f"{target}/vulnerable.php?id=1", "severity": "high", "confidence": "medium", "detail": "SQL error when payload sent"},
            {"type": "xss", "url": f"{target}/search?q=", "severity": "medium", "confidence": "low", "detail": "reflected script payload"}
        ]
    }
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(sample, f, indent=2)
    return sample

def run_xray(target: str, flags: List[str], out_json: Path) -> Dict[str, Any]:
    xray_bin = CONF.get("tools", {}).get("xray_path", "xray")
    if not tool_exists(xray_bin):
        console.print(f"[yellow]xray binary not found in PATH ('{xray_bin}'). Running mock output for testing.[/yellow]")
        time.sleep(0.6)
        return create_mock_output(target, out_json)

    cmd = build_xray_cmd(target, flags, out_json)
    console.print(f"[cyan]Executing:[/cyan] {' '.join(cmd)}")
    rc, stdout, stderr = run_command(cmd, timeout=CONF["defaults"].get("timeout"))
    # if xray produced a file, load it; else attempt to parse stdout as json
    if out_json.exists():
        try:
            with open(out_json, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"error": "failed to parse xray output file", "stdout": stdout, "stderr": stderr}
    else:
        # try to parse stdout
        try:
            return json.loads(stdout)
        except Exception:
            console.print("[red]Xray finished but no JSON output found; returning minimal feedback.[/red]")
            return {"stdout": stdout, "stderr": stderr}
