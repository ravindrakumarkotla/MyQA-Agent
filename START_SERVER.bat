@echo off
REM MyQA Agent - Windows Startup Script
REM Run this file to start the application

cls
echo.
echo ========================================
echo   MyQA Agent - Application Launcher
echo ========================================
echo.

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv .venv
    pause
    exit /b 1
)

REM Display information
echo Project Directory: %cd%
echo Python: .venv\Scripts\python.exe
echo Port: 8000
echo.
echo Starting server...
echo.

REM Start the application
.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000

pause
