@REM https://nuitka.net/user-documentation/user-manual.html
@REM Для имени: --output-filename=MyProgram
@REM Для иконки: --windows-icon-from-ico=resources\terminalWhite.ico
@REM Для PySide6: --enable-plugin=pyside6
@REM Отключает консоль: --windows-console-mode=disable

@echo off
cd /d "%~dp0"
call venv\Scripts\activate
set "PYTHONPATH=%CD%;%PYTHONPATH%"
python -m nuitka --onefile --standalone --follow-imports --jobs=4 --output-dir=compile --include-raw-dir=resources=resources src\Main.py
pause