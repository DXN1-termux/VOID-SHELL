import asyncio
import re

class IOInterceptor:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.stdout_buffer = []
        self.stderr_buffer = []

    async def stream_stdout(self, stream):
        while True:
            line = await stream.readline()
            if not line:
                break
            decoded = line.decode().strip()
            self.stdout_buffer.append(decoded)
            self.dashboard.display_stdout(decoded)

    async def stream_stderr(self, stream):
        while True:
            line = await stream.readline()
            if not line:
                break
            decoded = line.decode().strip()
            self.stderr_buffer.append(decoded)
            self.dashboard.display_stderr(decoded)

    def get_error_buffer(self) -> str:
        return "\n".join(self.stderr_buffer[-20:])
