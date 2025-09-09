from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

console = Console()

BANNER = r"""
$$$$$$$\  $$\   $$\ $$$$$$$\  $$\       $$$$$$\  $$$$$$\ $$$$$$$$\ 
$$  __$$\ $$ |  $$ |$$  __$$\ $$ |     $$  __$$\ \_$$  _|\__$$  __|
$$ |  $$ |\$$\ $$  |$$ |  $$ |$$ |     $$ /  $$ |  $$ |     $$ |   
$$ |  $$ | \$$$$  / $$$$$$$  |$$ |     $$ |  $$ |  $$ |     $$ |   
$$ |  $$ | $$  $$<  $$  ____/ $$ |     $$ |  $$ |  $$ |     $$ |   
$$ |  $$ |$$  /\$$\ $$ |      $$ |     $$ |  $$ |  $$ |     $$ |   
$$$$$$$  |$$ /  $$ |$$ |      $$$$$$$$\ $$$$$$  |$$$$$$\    $$ |   
\_______/ \__|  \__|\__|      \________|\______/ \______|   \__|                                                                      
                                                                   
       DXPLOIT.VulnScan — Find · Aggregate · Recommend
"""

def show_banner(version: str = "0.9.0"):
    console.clear()
    console.print(Panel(BANNER, title=f"DXPLOIT.VulnScan v{version}"))

def confirm_permission():
    console.print("[bold yellow]WARNING:[/bold yellow] Pastikan kamu memiliki izin eksplisit untuk melakukan pengujian terhadap target yang dipilih.")
    ans = console.input("Ketik 'YES' jika kamu memiliki izin (case-sensitive): ")
    if ans.strip() != "YES":
        console.print("[red]Konfirmasi izin tidak diberikan. Exiting.[/red]")
        raise SystemExit(1)

def get_progress():
    return Progress(SpinnerColumn(), TextColumn("{task.description}"), BarColumn(), TimeElapsedColumn())
