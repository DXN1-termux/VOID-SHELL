import asyncio
import time
from typing import List, Optional
from void_shell.core.interceptor import IOInterceptor
from void_shell.shadow.manager import ShadowManager
from void_shell.ai.reconstructor import NEREngine
from void_shell.tui.dashboard import Dashboard
from void_shell.memory.synapse import SynapseMemory
from void_shell.memory.recall import RecallEngine

class VoidEngine:
    """
    VoidEngine: The Central Nervous System of VOID-SHELL.
    Coordinates I/O, AI, Shadow Swarm, and Long-Term Memory.
    """
    def __init__(self, config):
        self.config = config
        self.dashboard = Dashboard(config)
        self.memory = SynapseMemory()
        self.recall_engine = RecallEngine(config)
        self.interceptor = IOInterceptor(self.dashboard)
        self.shadow_manager = ShadowManager(config, self.memory)
        self.ner_engine = NEREngine(config)

    async def run(self, cmd_args: List[str]):
        if not cmd_args:
            self.dashboard.show_banner()
            return

        # Check for Recall Command
        if cmd_args[0] == "recall" and len(cmd_args) > 1:
            query = " ".join(cmd_args[1:])
            await self.recall_engine.query(query)
            return

        full_cmd = " ".join(cmd_args)
        self.dashboard.log_execution(full_cmd)

        # 1. State Initialisation
        start_time = time.time()

        # 2. Process Execution Loop
        try:
            process = await asyncio.create_subprocess_shell(
                full_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Parallel Stream Interception
            await asyncio.gather(
                self.interceptor.stream_stdout(process.stdout),
                self.interceptor.stream_stderr(process.stderr)
            )

            return_code = await process.wait()
        except Exception as e:
            self.dashboard.display_stderr(f"Engine Fault: {str(e)}")
            return_code = -1

        duration = time.time() - start_time
        full_output = "\n".join(self.interceptor.stdout_buffer)

        # 3. Parallel Shadow Dispatch (Now with Output Awareness)
        shadow_task = asyncio.create_task(self.shadow_manager.dispatch(full_cmd, full_output))

        # 4. Intelligence Persistence
        cmd_id = self.memory.store_command(
            command=full_cmd,
            exit_code=return_code,
            duration=duration,
            summary="\n".join(self.interceptor.stdout_buffer[-5:]) # Last 5 lines as summary
        )

        # 5. Finalisation & Analysis
        await shadow_task
        self.dashboard.log_completion(return_code, duration)

        # 6. Indexing for Phase 2 Recall
        self.recall_engine.index_output(full_cmd, full_output)

        if return_code != 0:
            # Injecting recent context into NER Engine for high-precision fixing
            recent_context = self.memory.query_recent_context()
            await self.ner_engine.reconstruct(
                cmd=full_cmd, 
                error=self.interceptor.get_error_buffer(),
                context=recent_context
            )
