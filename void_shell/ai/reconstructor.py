import aiohttp
import json
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from void_shell.tui.dashboard import CONSOLE

class NEREngine:
    def __init__(self, config):
        self.config = config

    async def reconstruct(self, cmd: str, error: str, context: str = ""):
        if not self.config.features.auto_correct:
            return

        prompt = f"""
        🌌 VOID-SHELL: SYSTEM FAILURE DETECTED
        COMMAND: {cmd}
        ERROR: {error}
        CONTEXT: {context}
        TASK: Diagnose the Technical cause and provide a precision [PATCH].
        """

        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.config.ai.model,
                    "prompt": prompt,
                    "stream": False
                }
                
                with Progress(SpinnerColumn(), TextColumn("[void.ai]Consulting Abyss..."), console=CONSOLE, transient=True) as progress:
                    progress.add_task("AI", total=None)
                    async with session.post(self.config.ai.endpoint, json=payload) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            self.display_suggestion(data.get("response", ""))
        except Exception as e:
            CONSOLE.print(f"[void.error][!] NER Engine Synapse Failure: {str(e)}[/void.error]")

    def display_suggestion(self, suggestion: str):
        CONSOLE.print(Panel(suggestion, title="[void.ai]🌌 NEURAL RECONSTRUCTION[/void.ai]", border_style="void.ai"))
