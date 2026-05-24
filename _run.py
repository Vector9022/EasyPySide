from pathlib import Path
from _venv import BuildEnv, EnsureVenv, EnsureMain, VENV_PYTHON
import subprocess

MAIN_SCRIPT = Path("src") / "Main.py"

EnsureVenv()
EnsureMain(MAIN_SCRIPT)

subprocess.call([str(VENV_PYTHON), str(MAIN_SCRIPT)], env=BuildEnv())
input("\nНажмите Enter для выхода...")