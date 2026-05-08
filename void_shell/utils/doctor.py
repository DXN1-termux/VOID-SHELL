import sys
import os
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class VoidDoctor:
    def __init__(self):
        # Use centralized paths
        from void_shell.utils.paths import PROJECT_ROOT, CONFIG_PATH
        self.root_dir = PROJECT_ROOT
        self.config_path = CONFIG_PATH

    def diagnose_and_fix(self):
        console.print(Panel("🌌 [bold cyan]VOID-DOCTOR[/bold cyan]", border_style="cyan"))
        
        checks = [
            ("Python 3.10+", lambda: (sys.version_info >= (3, 10), "Update Python")),
            ("Dependencies", self.check_deps),
            ("Config Integrity", self.check_config),
            ("Module Map", self.check_modules)
        ]

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Component")
        table.add_column("Status")
        
        for name, check_func in checks:
            status, msg = check_func()
            table.add_row(name, "[green]PASS[/green]" if status else "[red]FAIL[/red]")

        console.print(table)

    def check_deps(self):
        try:
            import rich, questionary, aiohttp
            return True, ""
        except:
            return False, "Run install.sh"

    def check_config(self):
        return self.config_path.exists(), "Run 'v' to setup"

    def check_modules(self):
        return (self.root_dir / "void_shell" / "__init__.py").exists(), "Fixed init"

if __name__ == "__main__":
    VoidDoctor().diagnose_and_fix()
