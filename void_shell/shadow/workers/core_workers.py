import re
import socket
from void_shell.memory.synapse import SynapseMemory

class ScoutWorker:
    """
    Scout: The Passive Recon Specialist.
    Monitors traffic and automatically performs DNS/Port lookups.
    """
    def __init__(self, memory: SynapseMemory):
        self.memory = memory
        self.ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

    async def execute(self, cmd: str, stdout: str):
        # Extract IPs from command or output
        ips = self.ip_pattern.findall(cmd + " " + stdout)
        for ip in set(ips):
            # Non-blocking passive check
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                self.memory.store_finding(
                    finding_type="RECON_IP",
                    target=ip,
                    data={"hostname": hostname, "source": "Scout"}
                )
            except:
                pass

class GuardianWorker:
    """
    Guardian: The Leak Prevention Specialist.
    Scans output for high-entropy strings and credentials.
    """
    def __init__(self, memory: SynapseMemory):
        self.memory = memory
        # Common patterns for API Keys / Tokens
        self.secret_patterns = [
            re.compile(r'xox[baprs]-[0-9]{12}-[0-9]{12}-[a-z0-9]{24}', re.I), # Slack
            re.compile(r'gh[pous]_[a-zA-Z0-9]{36}', re.I), # GitHub
            re.compile(r'AIza[0-9A-Za-z-_]{35}', re.I), # Google
            re.compile(r'(?i)api_key[:=]\s*["\']([a-zA-Z0-9]{32,})["\']') # Generic
        ]

    async def execute(self, cmd: str, stdout: str):
        for pattern in self.secret_patterns:
            matches = pattern.findall(stdout)
            if matches:
                self.memory.store_finding(
                    finding_type="LEAK_ALERT",
                    target="internal",
                    data={"matches": len(matches), "worker": "Guardian", "risk": "CRITICAL"}
                )
