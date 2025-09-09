import json
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown
from .config import load_config

CONF = load_config()
console = Console()

def ensure_report_dir():
    rep = Path(CONF["defaults"].get("report_dir", "reports"))
    rep.mkdir(parents=True, exist_ok=True)
    return rep

def save_json_report(data: dict, target: str) -> Path:
    rep = ensure_report_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = str(target).replace("://", "_").replace("/", "_").replace(":", "_")
    path = rep / f"{ts}_{safe_target}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path

def save_md_report(data: dict, target: str) -> Path:
    rep = ensure_report_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = str(target).replace("://", "_").replace("/", "_").replace(":", "_")
    path = rep / f"{ts}_{safe_target}.md"
    lines = [f"# Report for {target}", f"Generated: {data.get('scan_date')}", "", "## Summary", f"- Total: {data.get('summary', {}).get('total_findings',0)}", f"- High: {data.get('summary', {}).get('high',0)}", f"- Medium: {data.get('summary', {}).get('medium',0)}", f"- Low: {data.get('summary', {}).get('low',0)}", "", "## Findings"]
    for f in data.get("findings", []):
        lines.append(f"### {f.get('id')} — {f.get('vuln_type')} ({f.get('severity')})")
        lines.append(f"- Location: `{f.get('location')}`")
        lines.append(f"- Confidence: {f.get('confidence')}")
        lines.append(f"- Recommendation: {f.get('recommended_action')}")
        lines.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return path
