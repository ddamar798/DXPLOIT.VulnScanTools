import yaml
from pathlib import Path

ROOT = Path.cwd()
CONFIG_PATH = ROOT / "config.yaml"

DEFAULTS = {
    "tools": {"xray_path": "xray"},
    "defaults": {"mode": "normal", "timeout": 3600, "report_dir": "reports", "write_html_report": False},
    "flags": {"normal": ["--basic-crawler"], "silent": ["--passive"], "brutal": ["--advanced-crawler", "--level", "high"]}
}

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            try:
                conf = yaml.safe_load(f) or {}
            except Exception:
                conf = {}
        # merge defaults
        merged = DEFAULTS.copy()
        merged.update(conf)
        return merged
    return DEFAULTS.copy()
