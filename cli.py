import argparse
from rich.console import Console
from .ui_utils import show_banner, confirm_permission
from .dxplot.mode_manager import get_mode_flags
from .plugins.xray_plugin import run_xray
from .parser.xray_parser import parse_xray_output
from .aggregator import aggregate_findings
from .recommender import recommend
from .reporter import save_report

console = Console()

def run_cli():
    parser = argparse.ArgumentParser(description="DXPLOIT.VulnScan CLI")
    parser.add_argument("--target", type=str, help="Target domain/IP")
    parser.add_argument("--mode", choices=["normal", "silent", "brutal"], default="normal")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation")
    args = parser.parse_args()

    show_banner()

    if not args.yes:
        confirm_permission()

    target = args.target or console.input("[cyan]Masukkan target (IP/Domain): [/cyan] ")
    mode_flags = get_mode_flags(args.mode)

    console.print(f"[bold green]Scanning target:[/bold green] {target} (mode={args.mode})")

    # Jalankan plugin Xray
    raw_output = run_xray(target, mode_flags)

    # Parse hasil
    findings = parse_xray_output(raw_output)

    # Aggregate & beri rekomendasi
    report_data = aggregate_findings(findings)
    report_data = recommend(report_data)

    # Simpan report
    save_report(report_data, target)

    console.print("[bold yellow]Scan selesai. Report tersimpan di folder reports/[/bold yellow]")
