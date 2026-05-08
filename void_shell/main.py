import sys
import asyncio
import os
from void_shell.core.engine import VoidEngine
from void_shell.utils.config import load_config
from void_shell.tui.dashboard import Dashboard
from void_shell.utils.wizard import VoidWizard

async def async_main():
    config_path = "config.json"
    
    # If no config, run wizard
    if not os.path.exists(config_path):
        wizard = VoidWizard()
        await wizard.run()
        # Reload config after wizard
    
    config = load_config(config_path)
    engine = VoidEngine(config)
    
    if len(sys.argv) < 2:
        Dashboard.show_banner()
        return

    cmd_args = sys.argv[1:]
    await engine.run(cmd_args)

def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
