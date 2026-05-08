import os
import json
import questionary
from rich.console import Console
from rich.panel import Panel

console = Console()

class VoidWizard:
    def __init__(self):
        self.config_path = "config.json"

    def run(self):
        console.print(Panel("🌌 [bold cyan]VOID-SHELL SETUP WIZARD[/bold cyan]\n[italic]Initializing Dark Matter Protocol...[/italic]", border_style="cyan"))

        # AI Configuration
        ai_provider = questionary.select(
            "Select your Intelligence Provider:",
            choices=["ollama", "groq", "openai"]
        ).ask()

        model = "qwen2.5-coder:0.5b"
        endpoint = "http://localhost:11434/api/generate"

        if ai_provider == "ollama":
            model = questionary.text("Ollama Model:", default="qwen2.5-coder:0.5b").ask()
            endpoint = questionary.text("Ollama Endpoint:", default="http://localhost:11434/api/generate").ask()
        
        features = questionary.checkbox(
            "Enable Abyssal Features:",
            choices=[
                questionary.Choice("Neural Error Reconstruction (NER)", checked=True),
                questionary.Choice("Shadow Swarm (Background Recon)", checked=True),
                questionary.Choice("Hyper-Reactive Overlays", checked=True),
                questionary.Choice("Stealth Mode", checked=False)
            ]
        ).ask()

        config = {
            "ai": {
                "provider": ai_provider,
                "model": model,
                "endpoint": endpoint,
                "temperature": 0.2,
                "max_tokens": 1024
            },
            "features": {
                "auto_correct": "Neural Error Reconstruction (NER)" in features,
                "shadow_execution": "Shadow Swarm (Background Recon)" in features,
                "neural_overlay": "Hyper-Reactive Overlays" in features,
                "stealth_mode": "Stealth Mode" in features
            },
            "system": {
                "log_level": "INFO",
                "max_parallel_workers": 8
            }
        }

        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)

        console.print("\n[bold green]✅ Dark Matter Protocol Initialized.[/bold green]")
        
        # Shell Integration Check
        if questionary.confirm("Inject alias 'v' into your shell profile?").ask():
            self.inject_alias()

    def inject_alias(self):
        home = os.path.expanduser("~")
        shell_configs = [".bashrc", ".zshrc"]
        alias_line = f"\nalias v='python3 -m void_shell.main'\n"
        
        for config in shell_configs:
            path = os.path.join(home, config)
            if os.path.exists(path):
                with open(path, "a") as f:
                    f.write(alias_line)
                console.print(f"[bold cyan]+ Added alias to {path}[/bold cyan]")
        
        console.print("[bold yellow]Please run 'source ~/.bashrc' or 'source ~/.zshrc' to apply changes.[/bold yellow]")
