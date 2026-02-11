@echo off
REM Automatic Launcher for Smart Surveillance System
REM This script handles the whitespace path issues automatically.

echo Starting Smart Surveillance System...
echo Note: Press 'Q' inside the video window to stop.

".venv\Scripts\python.exe" main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The program crashed or was stopped.
    echo If you see 'ModuleNotFoundError', please wait for installation to finish.
)
pause
