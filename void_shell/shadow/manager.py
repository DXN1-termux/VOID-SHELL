import asyncio
from typing import List

from void_shell.shadow.workers.core_workers import ScoutWorker, GuardianWorker

class ShadowManager:
    def __init__(self, config, memory):
        self.config = config
        self.memory = memory
        self.scout = ScoutWorker(memory)
        self.guardian = GuardianWorker(memory)

    async def dispatch(self, cmd: str, stdout: str = ""):
        """Dispatches the shadow swarm to gather intelligence."""
        if not self.config.features.shadow_execution:
            return

        # Run workers in parallel
        await asyncio.gather(
            self.scout.execute(cmd, stdout),
            self.guardian.execute(cmd, stdout)
        )
