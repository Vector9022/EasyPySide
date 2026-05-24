import os
import sys
import subprocess
from pathlib import Path

PYTHON_VERSION = "3.12"
VENV_DIR = Path("venv")
VENV_PYTHON = VENV_DIR / "Scripts" / "python.exe"

def BuildEnv():
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = str(VENV_DIR.resolve())
    env["PATH"] = str((VENV_DIR / "Scripts").resolve()) + os.pathsep + env["PATH"] # PATH
    env["PYTHONPATH"] = str(Path.cwd()) + os.pathsep + env.get("PYTHONPATH", "") # PYTHONPATH
    return env

def EnsureVenv():
    if not VENV_DIR.exists():
        print("Создание виртуального окружения...")

        try:
            result = subprocess.run(
                ["py", f"-{PYTHON_VERSION}", "-c", "import sys; print(sys.executable)"],
                capture_output=True,
                text=True,
                check=True
            )
            pythonExe = result.stdout.strip()
        except Exception:
            print(f"Не удалось найти Python {PYTHON_VERSION}, используется \"{sys.executable}\".")
            pythonExe = sys.executable

        subprocess.check_call([pythonExe, "-m", "venv", str(VENV_DIR)])

        reqFile = Path("requirements.txt")
        if reqFile.exists():
            print("Установка зависимостей...")
            subprocess.check_call([str(VENV_PYTHON), "-m", "pip", "install", "-r", str(reqFile)])

def EnsureMain(mainScript):
    if not mainScript.exists():
        print(f"Файл {mainScript} не найден.")
        input("Нажмите Enter для выхода...")
        exit(1)

if __name__ == "__main__":
    EnsureVenv()
    print("Запуск CMD с виртуальным окружением...")
    subprocess.call("cmd.exe", env=BuildEnv())