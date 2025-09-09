import subprocess
import shutil
from pathlib import Path
from typing import List, Tuple
from .config import load_config

CONF = load_config()

def tool_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None

def run_command(cmd: List[str], timeout: int = None) -> Tuple[int, str, str]:
    """
    Run subprocess command, return (returncode, stdout, stderr)
    """
    timeout = timeout or CONF["defaults"].get("timeout", 3600)
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as e:
        return 124, "", f"TimeoutExpired: {e}"
    except Exception as e:
        return 1, "", f"Exception: {e}"
