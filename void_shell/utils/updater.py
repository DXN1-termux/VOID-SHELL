import os
import subprocess
from rich.console import Console

console = Console()

class VoidUpdater:
    """
    VOID-UPDATER: Automated protocol synchronization.
    Checks for remote changes and pulls them if available.
    """
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def check_and_update(self):
        if not os.path.exists(os.path.join(self.root_dir, ".git")):
            return

        try:
            # Check for remote updates without pulling
            subprocess.check_call(["git", "fetch", "origin"], cwd=self.root_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Compare local branch with remote
            status = subprocess.check_output(["git", "status", "-uno"], cwd=self.root_dir).decode()
            
            if "Your branch is behind" in status:
                console.print("[void.info]🌌 New Dark Matter Protocol detected. Updating...[/void.info]")
                subprocess.check_call(["git", "pull", "origin", "master"], cwd=self.root_dir)
                console.print("[bold green]✅ VOID-SHELL has evolved to the latest version.[/bold green]")
                # We might need to restart if core files changed, but for now just continue
        except Exception as e:
            # Silent fail for updates to avoid blocking the user
            pass
