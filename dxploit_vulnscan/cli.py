"""
Main CLI orchestration module.
"""
import argparse
from pathlib import Path
import time
from .ui_utils import show_banner, confirm_permission, get_progress, console
from .mode_manager import get_mode_flags
from .plugins.xray_plugin import run_xray
from .parser.xray_parser import parse_xray_raw
from .aggregator import aggregate
from .reporter import save_json_report, save_md_report
from .config import load_config

CONF = load_config()

def run_cli():
    parser = argparse.ArgumentParser(prog="DXPLOIT.VulnScan", description="DXPLOIT.VulnScan — Wrapper Scanner (Xray) MVP")
    parser.add_argument("--target", "-t", help="Target domain/URL or IP (comma separated for multiple)")
    parser.add_argument("--mode", "-m", choices=["normal", "silent", "brutal"], help="Scan mode")
    parser.add_argument("--yes", action="store_true", help="Auto confirm permission")
    args = parser.parse_args()

    show_banner()
    if not args.yes:
        try:
            confirm_permission()
        except SystemExit:
            return

    mode_choice = args.mode or CONF["defaults"].get("mode", "normal")
    mode, flags = get_mode_flags(mode_choice)
    console.print(f"[green]Mode:[/green] {mode.upper()}")

    targets = []
    if args.target:
        if "," in args.target:
            targets = [t.strip() for t in args.target.split(",") if t.strip()]
        elif Path(args.target).exists():
            # file of targets
            with open(args.target, "r", encoding="utf-8") as f:
                targets = [l.strip() for l in f if l.strip()]
        else:
            targets = [args.target.strip()]
    else:
        t = console.input("Masukkan target (URL or IP). For batch, separate by comma or point to file: ")
        if "," in t:
            targets = [x.strip() for x in t.split(",") if x.strip()]
        else:
            targets = [t.strip()]

    # Run sequentially (MVP)
    for target in targets:
        console.print(f"[bold cyan]Starting scan for:[/bold cyan] {target}")
        # prepare out file path
        rep_dir = Path(CONF["defaults"].get("report_dir", "reports"))
        rep_dir.mkdir(exist_ok=True)
        out_json = rep_dir / f"raw_{str(target).replace('://','_').replace('/','_')}_{int(time.time())}.json"
        # progress
        with get_progress() as progress:
            task = progress.add_task("Running scanner", total=None)
            result = run_xray(target, flags, out_json)
            progress.update(task, description="Parsing results")
            time.sleep(0.3)
            parsed = parse_xray_raw(result)
            progress.update(task, description="Aggregating findings")
            time.sleep(0.3)
            aggregated = aggregate(parsed)
            # save reports
            json_path = save_json_report(aggregated, target)
            md_path = save_md_report(aggregated, target)
            progress.update(task, description="Done — reports written")
            time.sleep(0.2)
        # print short summary
        from rich.table import Table
        table = Table(title=f"Findings — {target}")
        table.add_column("ID", style="cyan")
        table.add_column("Type")
        table.add_column("Severity")
        table.add_column("Location")
        table.add_column("Recommendation")
        for f in aggregated.get("findings", []):
            table.add_row(f.get("id"), str(f.get("vuln_type")), str(f.get("severity")), str(f.get("location")), str(f.get("recommended_action") or "-"))
        console.print(table)
        console.print(f"[green]Reports saved:[/green] {json_path}  {md_path}")

    console.print("[bold green]All tasks finished.[/bold green]")
