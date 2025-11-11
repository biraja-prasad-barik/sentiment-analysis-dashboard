@echo off
REM Simple Development Server Startup Script
REM Run with: START_DEV.bat

echo ========================================
echo   Sentiment Analysis Dashboard - DEV
echo ========================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Check if virtual environment exists
if exist ".venv\" (
    echo [OK] Virtual environment found
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo [INFO] No virtual environment found
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo [OK] Virtual environment created
)
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements_file/requirements_dev.txt --quiet
echo [OK] Dependencies installed
echo.

REM Run the application
echo ========================================
echo   Starting Development Server...
echo ========================================
echo.
echo URL: http://localhost:5000
echo Mode: Development
echo Database: SQLite (sentiment_dev.db)
echo.
echo Press Ctrl+C to stop the server
echo.

python app_dev.py
