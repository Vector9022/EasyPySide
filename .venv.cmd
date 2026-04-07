@echo off
cd /d "%~dp0"
set "NEWVENV=0"
if not exist "venv\" (
    py -3.12 -m venv venv
    set "NEWVENV=1"
)
call "venv\Scripts\activate.bat"
if "%NEWVENV%"=="1" python -m pip install -r "requirements.txt"
set "PYTHONPATH=%CD%;%PYTHONPATH%"
cmd