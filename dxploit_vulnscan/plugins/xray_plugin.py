"""
xray_plugin.py — integrated runner for Xray within DXPLOIT.VulnScan

Behavior:
- Read config (xray_path, xray_config_dir) from dxploit_vulnscan.config.
- Run Xray from the config dir (cwd) so xray loads xray.yaml/module.xray.yaml/plugin.xray.yaml.
- Output JSON saved to project's reports directory (safe path).
- On missing binary or runtime error, fall back to mock output for development/testing.
"""

from pathlib import Path
import json
import subprocess
import shlex
import time
from typing import List, Dict, Any, Tuple

from ..config import load_config
from ..ui_utils import console

CONF = load_config()

def _get_paths() -> Tuple[str, Path]:
    """
    Return (xray_bin_path, xray_config_dir_path)
    """
    xray_bin = CONF.get("tools", {}).get("xray_path", "xray")
    xray_conf_dir = Path(CONF.get("tools", {}).get("xray_config_dir", "/usr/local/share/xray"))
    return xray_bin, xray_conf_dir

def _ensure_report_dir() -> Path:
    rep = Path(CONF["defaults"].get("report_dir", "reports"))
    rep.mkdir(parents=True, exist_ok=True)
    return rep

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

def _run_subprocess(cmd: List[str], cwd: Path = None, timeout: int = 3600) -> Tuple[int, str, str]:
    """
    Run subprocess with given cwd and return (rc, stdout, stderr)
    """
    try:
        console.log(f"[cyan]Running:[/cyan] {' '.join(shlex.quote(x) for x in cmd)} (cwd={cwd})")
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=str(cwd) if cwd else None, timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as e:
        return 124, "", f"TimeoutExpired: {e}"
    except Exception as e:
        return 1, "", f"Exception: {e}"

def tool_exists(path_str: str) -> bool:
    # If given as absolute path, check file exists and is executable.
    p = Path(path_str)
    if p.is_file():
        return p.stat().st_mode & 0o111 != 0
    # fallback: check by name in PATH
    from shutil import which
    return which(path_str) is not None

def build_xray_cmd(xray_bin: str, target: str, flags: List[str], out_json: Path) -> List[str]:
    """
    Build command list to run Xray.
    NOTE: we run webscan as subcommand; flags are appended after webscan-specific args.
    """
    # prefer using --url (or -u) for single url
    cmd = [xray_bin, "webscan", "--basic-crawler", target, "--json-output", str(out_json)]
    # append additional flags (if any)
    if flags:
        cmd.extend(flags)
    return cmd

def run_xray(target: str, flags: List[str], out_json: Path) -> Dict[str, Any]:
    """
    Run xray and return parsed JSON (dict) OR a dict with keys stdout/stderr on failure.
    - target: url or ip (string)
    - flags: list of xray-specific flags (from mode manager)
    - out_json: Path where xray should write its json output (we expect xray to create this)
    """
    xray_bin, xray_conf_dir = _get_paths()
    rep_dir = _ensure_report_dir()
    # If out_json is not under reports, move it into reports to keep consistency
    if not str(out_json).startswith(str(rep_dir)):
        ts = int(time.time())
        safe_target = str(target).replace("://", "_").replace("/", "_").replace(":", "_")
        out_json = rep_dir / f"xray_{safe_target}_{ts}.json"

    # If binary not found / not executable -> fallback mock
    if not tool_exists(xray_bin):
        console.print(f"[yellow]xray binary not found or not executable ('{xray_bin}'). Running mock output for testing.[/yellow]")
        return create_mock_output(target, out_json)

    # Ensure config dir exists
    if not xray_conf_dir.exists():
        console.print(f"[yellow]xray config dir not found ('{xray_conf_dir}'). Running binary from its folder if possible.[/yellow]")
        # attempt to run with cwd None; still possible
        xray_conf_dir = None

    # Build cmd; we intentionally *do not* use global --config flag because many xray versions read config from CWD
    cmd = build_xray_cmd(xray_bin, target, flags, out_json)

    # Run with cwd = xray_conf_dir (so xray picks up xray.yaml)
    rc, stdout, stderr = _run_subprocess(cmd, cwd=xray_conf_dir, timeout=CONF["defaults"].get("timeout", 3600))

    # If file produced, try load it
    if out_json.exists():
        try:
            with open(out_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            console.print(f"[red]Failed to parse xray JSON output: {e}[/red]")
            return {"error": "failed to parse xray output file", "stdout": stdout, "stderr": stderr}
    else:
        # No file produced. Return stdout/stderr for debugging (and also produce mock if rc != 0)
        console.print(f"[yellow]Xray finished but JSON file not found. rc={rc} stdout_len={len(stdout)} stderr_len={len(stderr)}[/yellow]")
        # If rc == 0 but no file, attempt to parse stdout as json
        try:
            parsed = json.loads(stdout)
            return parsed
        except Exception:
            # fallback to mock (but save stdout/stderr to a debug file)
            debug_path = rep_dir / f"xray_debug_{int(time.time())}.log"
            with open(debug_path, "w", encoding="utf-8") as fh:
                fh.write("=== STDOUT ===\n")
                fh.write(stdout or "")
                fh.write("\n\n=== STDERR ===\n")
                fh.write(stderr or "")
            console.print(f"[yellow]Saved debug output to {debug_path}[/yellow]")
            return {"error": "no json output", "stdout": stdout, "stderr": stderr, "debug_log": str(debug_path)}
