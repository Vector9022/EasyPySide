@echo off
cd /d "%~dp0"
call venv\Scripts\activate
set "PYTHONPATH=%CD%;%PYTHONPATH%"

chcp 65001 >nul
echo [REM] pip "install, uninstall, upgrade" "название пакета"
echo.

:ask
set /p action=pip 

for /f "tokens=1,2 delims= " %%a in ("%action%") do (
    set first=%%a
    set second=%%b
)

if /i "%first%"=="install" goto valid
if /i "%first%"=="uninstall" goto valid
if /i "%first%"=="upgrade" (
    set first=install --upgrade
    goto valid
)

echo [ERROR] Допустимы только "install, uninstall, upgrade"
echo.
goto ask

:valid
chcp 866 >nul
pip %first% %second%
pip freeze > requirements.txt

pause