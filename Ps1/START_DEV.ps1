# Simple Development Server Startup Script
# Run with: .\START_DEV.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Sentiment Analysis Dashboard - DEV" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Check if virtual environment exists
if (Test-Path ".venv") {
    Write-Host "✓ Virtual environment found" -ForegroundColor Green
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "! No virtual environment found" -ForegroundColor Yellow
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    & .\.venv\Scripts\Activate.ps1
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements_file/requirements_dev.txt --quiet
Write-Host "✓ Dependencies installed" -ForegroundColor Green

Write-Host ""

# Run the application
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Development Server..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 URL: http://localhost:5000" -ForegroundColor Green
Write-Host "🔧 Mode: Development" -ForegroundColor Green
Write-Host "💾 Database: SQLite (sentiment_dev.db)" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python app_dev.py
