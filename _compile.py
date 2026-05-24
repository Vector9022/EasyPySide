from pathlib import Path
from _venv import BuildEnv, EnsureVenv, EnsureMain, VENV_PYTHON
import subprocess

MAIN_SCRIPT = Path("src") / "Main.py"

EnsureVenv()
EnsureMain(MAIN_SCRIPT)

cmd = [
    "-m", "nuitka",
    "--onefile",
    "--standalone",
    "--follow-imports",
    "--jobs=4",
    "--output-dir=compile",
    "--include-raw-dir=resources=resources",
    "--output-filename=MyProgram",
    "--windows-icon-from-ico=resources/terminalWhite.ico",
    "--enable-plugin=pyside6", # Для PySide6
    str(MAIN_SCRIPT)
]

subprocess.call([str(VENV_PYTHON), *cmd], env=BuildEnv())
input("\nНажмите Enter для выхода...")