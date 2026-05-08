import re
from rich.text import Text

class NeuralOverlay:
    def __init__(self, config):
        self.config = config
        self.patterns = [
            (r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', "bold green"), # IPs
            (r'(https?://[^\s]+)', "underline blue"), # URLs
            (r'(error|failed|failure|critical)', "bold red"), # Errors
            (r'(success|completed|started|initiating)', "bold cyan"), # Events
            (r'(:\d{2,5})', "bold yellow"), # Ports
            (r'(0x[0-9a-fA-F]+)', "italic magenta"), # Hex/Memory
            (r'(\[[A-Z_]+\])', "bold white on black"), # Log tags
        ]

    def process(self, text: str) -> Text:
        rich_text = Text(text)
        
        if not self.config.features.neural_overlay:
            return rich_text

        for pattern, style in self.patterns:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            for match in matches:
                start, end = match.span()
                rich_text.stylize(style, start, end)
        
        return rich_text
