import aiohttp
import json
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

class NEREngine:
    def __init__(self, config):
        self.config = config

    async def reconstruct(self, cmd: str, error: str, context: str = ""):
        """Neural Error Reconstruction - The core of VOID-SHELL's self-healing."""
        if not self.config.features.auto_correct:
            return

        prompt = f"""
        🌌 VOID-SHELL: SYSTEM FAILURE DETECTED
        
        COMMAND ATTEMPTED: {cmd}
        ERROR LOG:
        {error}
        
        RECENT HISTORICAL CONTEXT:
        {context}
        
        TASK: 
        1. Diagnose the technical root cause (taking history into account).
        2. Synthesize a precision patch (corrected command).
        3. Explain the logic briefly.
        
        FORMAT:
        [DIAGNOSIS]: <reason>
        [PATCH]: <corrected_command>
        [LOGIC]: <brief_explanation>
        """

        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.config.ai.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.config.ai.temperature,
                        "num_predict": self.config.ai.max_tokens
                    }
                }
                
                # We'll use a progress bar for that "Advanced" feel
                from void_shell.tui.dashboard import CONSOLE
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[void.ai]Consulting the Dark Matter Core...[/void.ai]"),
                    console=CONSOLE,
                    transient=True
                ) as progress:
                    progress.add_task("AI", total=None)
                    async with session.post(self.config.ai.endpoint, json=payload) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            response = data.get("response", "The Void remains silent.")
                            self.display_suggestion(response)
                        else:
                            CONSOLE.print("[void.error][!] Dark Matter Core unreachable.[/void.error]")
        except Exception as e:
            from void_shell.tui.dashboard import CONSOLE
            CONSOLE.print(f"[void.error][!] Synapse Failure: {str(e)}[/void.error]")

    def display_suggestion(self, suggestion: str):
        from void_shell.tui.dashboard import CONSOLE
        CONSOLE.print(Panel(
            suggestion,
            title="[void.ai]🌌 NEURAL RECONSTRUCTION[/void.ai]",
            border_style="void.ai",
            padding=(1, 2)
        ))
        # Logic for "Hit Enter to Apply" would go here in a more advanced version
