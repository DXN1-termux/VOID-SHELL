import socket
import asyncio
import json
from void_shell.memory.synapse import SynapseMemory

class SynapseSync:
    """
    Synapse P2P: Distributed Intelligence Synchronization.
    Uses UDP broadcast for local peer discovery and sharing.
    """
    def __init__(self, memory: SynapseMemory, port: int = 42424):
        self.memory = memory
        self.port = port
        self.running = False

    async def start_broadcaster(self):
        """Broadcasts current findings to the local network."""
        self.running = True
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        while self.running:
            # Broadcast recent findings
            # (In a real elite env, this would be encrypted)
            data = {"type": "SYNC_BEACON", "id": socket.gethostname()}
            sock.sendto(json.dumps(data).encode(), ('<broadcast>', self.port))
            await asyncio.sleep(60) # Heartbeat

    async def start_listener(self):
        """Listens for intelligence from other VOID-SHELL instances."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', self.port))
        sock.setblocking(False)
        
        loop = asyncio.get_event_loop()
        while self.running:
            data, addr = await loop.sock_recvfrom(sock, 1024)
            msg = json.loads(data.decode())
            if msg.get("type") == "SYNC_DATA":
                self.memory.store_finding(
                    finding_type="REMOTE_SYNC",
                    target=msg["origin"],
                    data=msg["payload"]
                )
