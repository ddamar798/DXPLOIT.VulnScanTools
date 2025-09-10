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
    parser = argparse.ArgumentParser(
        prog="DXPLOIT.VulnScan",
        description="DXPLOIT.VulnScan — Wrapper Scanner (Xray) MVP"
    )
    parser.add_argument("--target", "-t", help="Target domain/URL or IP (comma separated for multiple)")
    parser.add_argument("--mode", "-m", choices=["normal", "silent", "brutal"], help="Scan mode")
    parser.add_argument("--yes", action="store_true", help="Auto confirm permission")
    args = parser.parse_args()

    # Banner
    show_banner()

    # Konfirmasi izin
    if not args.yes:
        try:
            confirm_permission()
        except SystemExit:
            return

    # Input target
    targets = []
    if args.target:
        if "," in args.target:
            targets = [t.strip() for t in args.target.split(",") if t.strip()]
        elif Path(args.target).exists():
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

    # Pilih mode scanning
    if args.mode:
        mode_choice = args.mode
    else:
        console.print("\n[bold cyan]Pilih Mode Scanning:[/bold cyan]")
        console.print("1. Normal")
        console.print("2. Silent")
        console.print("3. Brutal")
        choice = console.input("Pilih (1/2/3): ").strip()

        if choice == "1":
            mode_choice = "normal"
        elif choice == "2":
            mode_choice = "silent"
        elif choice == "3":
            mode_choice = "brutal"
        else:
            console.print("[yellow]Pilihan tidak valid, default ke Normal.[/yellow]")
            mode_choice = "normal"

    mode, flags = get_mode_flags(mode_choice)
    console.print(f"[green]Mode:[/green] {mode.upper()}")

    # Jalankan scan per target
    for target in targets:
        console.print(f"[bold cyan]Starting scan for:[/bold cyan] {target}")

        rep_dir = Path(CONF["defaults"].get("report_dir", "reports"))
        rep_dir.mkdir(exist_ok=True)
        out_json = rep_dir / f"raw_{str(target).replace('://','_').replace('/','_')}_{int(time.time())}.json"

        with get_progress() as progress:
            task = progress.add_task("Running scanner", total=None)
            result = run_xray(target, flags, out_json)

            progress.update(task, description="Parsing results")
            time.sleep(0.3)
            parsed = parse_xray_raw(result)

            progress.update(task, description="Aggregating findings")
            time.sleep(0.3)
            aggregated = aggregate(parsed)

            # Save reports
            json_path = save_json_report(aggregated, target)
            md_path = save_md_report(aggregated, target)

            progress.update(task, description="Done — reports written")
            time.sleep(0.2)

        # Tampilkan ringkasan hasil
        from rich.table import Table
        table = Table(title=f"Findings — {target}")
        table.add_column("ID", style="cyan")
        table.add_column("Type")
        table.add_column("Severity")
        table.add_column("Location")
        table.add_column("Recommendation")

        for f in aggregated.get("findings", []):
            table.add_row(
                f.get("id"),
                str(f.get("vuln_type")),
                str(f.get("severity")),
                str(f.get("location")),
                str(f.get("recommended_action") or "-")
            )

        console.print(table)
        console.print(f"[green]Reports saved:[/green] {json_path}  {md_path}")

    console.print("[bold green]All tasks finished.[/bold green]")
