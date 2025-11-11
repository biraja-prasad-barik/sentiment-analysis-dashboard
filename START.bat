@echo off
REM Quick Start Script - Double-click to run!

echo ========================================
echo   Sentiment Analysis Dashboard
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Install dependencies
echo Installing dependencies (first time only)...
pip install -r requirements_file/requirements_dev.txt --quiet --disable-pip-version-check
echo [OK] Dependencies ready
echo.

REM Start server
echo ========================================
echo   Starting Server...
echo ========================================
echo.
echo Open your browser at: http://localhost:5000
echo.
echo Press Ctrl+C to stop
echo.

REM Open browser after 3 seconds
start /B timeout /t 3 /nobreak >nul && start http://localhost:5000

REM Run app
python app_dev.py
