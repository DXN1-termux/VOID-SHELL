import sys
import asyncio
from void_shell.core.engine import VoidEngine
from void_shell.utils.config import load_config
from void_shell.tui.dashboard import Dashboard

async def async_main():
    config = load_config()
    engine = VoidEngine(config)
    
    if len(sys.argv) < 2:
        # Show banner/help
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
