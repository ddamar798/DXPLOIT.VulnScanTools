from rich.console import Console
from rich.panel import Panel

console = Console()

def show_banner():
    banner = r"""
██████╗ ██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██║  ██║██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝███████║██████╔╝██║     ██║   ██║██║   ██║   
██╔═══╝ ██╔══██║██╔═══╝ ██║     ██║   ██║██║   ██║   
██║     ██║  ██║██║     ███████╗╚██████╔╝██║   ██║   
╚═╝     ╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
"""
    console.print(Panel(banner, title="DXPLOIT.VulnScan", subtitle="Find · Aggregate · Recommend"))

def confirm_permission():
    ans = console.input("[red]Pastikan Anda memiliki izin eksplisit untuk scan! Ketik YES untuk lanjut: [/red] ")
    if ans.strip().upper() != "YES":
        console.print("[bold red]Dibatalkan.[/bold red]")
        exit(1)
