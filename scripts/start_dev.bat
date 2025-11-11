@echo off
REM Start development environment on Windows

echo Starting development environment...

REM Check if Redis is running
redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo Redis is not running. Please start Redis first.
    echo Download from: https://github.com/microsoftarchive/redis/releases
    pause
    exit /b 1
)

REM Start Celery worker in new window
start "Celery Worker" cmd /k celery -A core.celery_app worker --loglevel=info --pool=solo

REM Start Celery beat in new window
start "Celery Beat" cmd /k celery -A core.celery_app beat --loglevel=info

REM Wait a bit for workers to start
timeout /t 3 /nobreak >nul

REM Start Flask app
set FLASK_ENV=development
python app_production.py

pause
