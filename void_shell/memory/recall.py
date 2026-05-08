import asyncio
from void_shell.memory.vector_store import VectorStore
from void_shell.tui.dashboard import CONSOLE
from rich.panel import Panel

class RecallEngine:
    """
    The Recall Engine: Interrogates the Synapse Vector Store using Natural Language.
    """
    def __init__(self, config):
        self.config = config
        self.vector_store = VectorStore()

    async def query(self, user_query: str):
        CONSOLE.print(f"[void.ai]🌌 Interrogating Synapse for: '{user_query}'...[/void.ai]")
        
        # 1. Semantic Search in Vector Store
        results = self.vector_store.search(user_query)

        if not results:
            CONSOLE.print("[void.warn][!] No semantic matches found in the Abyss.[/void.warn]")
            return

        # 2. Present findings
        for i, res in enumerate(results):
            text = res["text"]
            metadata = res["metadata"]
            CONSOLE.print(Panel(
                f"[bold white]{text}[/bold white]\n\n[dim]Source: {metadata.get('command', 'unknown')}[/dim]",
                title=f"[void.overlay]Match {i+1}[/void.overlay]",
                border_style="void.overlay"
            ))

    def index_output(self, command: str, output: str):
        """Indexes terminal output for future recall."""
        # Split output into meaningful chunks
        chunks = [output[i:i+500] for i in range(0, len(output), 500)]
        for chunk in chunks:
            self.vector_store.add_fragment(
                text=chunk,
                metadata={"command": command}
            )
