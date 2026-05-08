import asyncio
import time
from typing import List
from void_shell.core.interceptor import IOInterceptor
from void_shell.shadow.manager import ShadowManager
from void_shell.ai.reconstructor import NEREngine
from void_shell.tui.dashboard import Dashboard

class VoidEngine:
    def __init__(self, config):
        self.config = config
        self.dashboard = Dashboard(config)
        self.interceptor = IOInterceptor(self.dashboard)
        self.shadow_manager = ShadowManager(config)
        self.ner_engine = NEREngine(config)

    async def run(self, cmd_args: List[str]):
        full_cmd = " ".join(cmd_args)
        self.dashboard.log_execution(full_cmd)

        # Start Shadow Swarm
        shadow_task = asyncio.create_task(self.shadow_manager.dispatch(full_cmd))

        # Start Subprocess
        start_time = time.time()
        process = await asyncio.create_subprocess_shell(
            full_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Intercept I/O
        await asyncio.gather(
            self.interceptor.stream_stdout(process.stdout),
            self.interceptor.stream_stderr(process.stderr)
        )

        return_code = await process.wait()
        duration = time.time() - start_time
        
        await shadow_task
        self.dashboard.log_completion(return_code, duration)

        if return_code != 0:
            await self.ner_engine.reconstruct(full_cmd, self.interceptor.get_error_buffer())
