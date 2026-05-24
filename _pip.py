import localLib.RAA as RAA; RAA.RunAsAdmin()
from _venv import BuildEnv, EnsureVenv, VENV_PYTHON
import subprocess

env = BuildEnv()
EnsureVenv()

print('[INFO] Доступные команды: install | uninstall | upgrade')

while True:
    try:
        action = input("\npip ").strip()
        if not action:
            continue

        parts = action.split(maxsplit=1)
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "upgrade":
            subprocess.call([str(VENV_PYTHON), *["-m", "pip", "install", "--upgrade", arg]], env=env)
        elif cmd in ("install", "uninstall"):
            subprocess.call([str(VENV_PYTHON), *["-m", "pip", cmd, arg]], env=env)
        else:
            continue

        with open("requirements.txt", "w", encoding="utf-8") as f:
            subprocess.call(
                [str(VENV_PYTHON), "-m", "pip", "freeze"],
                stdout=f,
                env=env
            )

    except KeyboardInterrupt:
        break

input("\nНажмите Enter для выхода...")