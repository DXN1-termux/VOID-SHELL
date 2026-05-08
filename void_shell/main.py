import sys
import asyncio
import os
from void_shell.utils.paths import CONFIG_PATH
from void_shell.utils.doctor import VoidDoctor
def main():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")

    # 1. Automatic Update Check
    from void_shell.utils.updater import VoidUpdater
    updater = VoidUpdater()
    updater.check_and_update()

    # 2. Check for 'doctor' command
    if len(sys.argv) > 1 and sys.argv[1] == "doctor":
        from void_shell.utils.doctor import VoidDoctor
        doctor = VoidDoctor()
        doctor.diagnose_and_fix()
        return

    # 3. Handle setup if needed
    if not os.path.exists(config_path):
        from void_shell.utils.wizard import VoidWizard
        wizard = VoidWizard()
        wizard.run()

    # 4. Async Execution (The actual engine)
    async def run_engine():
        from void_shell.utils.config import load_config
        from void_shell.core.engine import VoidEngine
        from void_shell.tui.dashboard import Dashboard

        config = load_config(config_path)
        engine = VoidEngine(config)

        if len(sys.argv) < 2:
            Dashboard.show_banner()
            return

        cmd_args = sys.argv[1:]
        await engine.run(cmd_args)

    try:
        asyncio.run(run_engine())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"🌌 [VOID] Runtime Crash: {str(e)}")
        from void_shell.utils.doctor import VoidDoctor
        VoidDoctor().diagnose_and_fix()


if __name__ == "__main__":
    main()
