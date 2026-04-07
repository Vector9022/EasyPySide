@echo off
cd /d "%~dp0"
call venv\Scripts\activate
set "PYTHONPATH=%CD%;%PYTHONPATH%"
python src\Main.py
pause