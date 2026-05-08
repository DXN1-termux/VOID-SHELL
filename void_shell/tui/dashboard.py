from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme
from void_shell.tui.overlay import NeuralOverlay
import re

VOID_THEME = Theme({
    "void.base": "cyan",
    "void.warn": "bold yellow",
    "void.error": "bold red",
    "void.info": "italic blue",
    "void.ai": "bold magenta",
    "void.overlay": "bold green on black"
})

CONSOLE = Console(theme=VOID_THEME)

class Dashboard:
    def __init__(self, config):
        self.config = config
        self.console = CONSOLE
        self.overlay = NeuralOverlay(config)

    @staticmethod
    def show_banner():
        console = Console(theme=VOID_THEME)
        banner = """
        🌌 VOID-SHELL: THE DARK MATTER PROTOCOL
        "In the silence of the void, the machine speaks."
        """
        console.print(Panel(banner, border_style="void.base", expand=False))

    def log_execution(self, cmd: str):
        self.console.print(f"[void.base]🌌 Protocol Initiated:[/void.base] [bold white]{cmd}[/bold white]")

    def display_stdout(self, line: str):
        processed_text = self.overlay.process(line)
        self.console.print(processed_text)

    def display_stderr(self, line: str):
        self.console.print(f"[void.error][!] {line}[/void.error]")

    def log_completion(self, code: int, duration: float):
        style = "void.info" if code == 0 else "void.error"
        self.console.print(f"\n[{style}]🌌 Process terminated | Code: {code} | Time: {duration:.2f}s[/{style}]")
