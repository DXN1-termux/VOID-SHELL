from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme
import re

VOID_THEME = Theme({
    "void.base": "cyan",
    "void.warn": "bold yellow",
    "void.error": "bold red",
    "void.info": "italic blue",
    "void.ai": "bold magenta",
    "void.overlay": "bold green on black"
})

class Dashboard:
    def __init__(self, config):
        self.config = config
        self.console = Console(theme=VOID_THEME)

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
        # Apply basic highlighting here or delegate to Overlays
        highlighted = self.apply_simple_highlights(line)
        self.console.print(highlighted)

    def display_stderr(self, line: str):
        self.console.print(f"[void.error][!] {line}[/void.error]")

    def log_completion(self, code: int, duration: float):
        style = "void.info" if code == 0 else "void.error"
        self.console.print(f"\n[{style}]🌌 Process terminated | Code: {code} | Time: {duration:.2f}s[/{style}]")

    def apply_simple_highlights(self, text: str) -> str:
        # Neural Overlay logic placeholder
        text = re.sub(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', r'[void.overlay]\1[/void.overlay]', text)
        return text
