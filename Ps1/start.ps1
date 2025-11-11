# PowerShell startup script for Sentiment Analysis App

Clear-Host

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   SENTIMENT ANALYSIS WEB APPLICATION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting the application..." -ForegroundColor Green
Write-Host ""
Write-Host "Please wait while dependencies load..." -ForegroundColor Yellow
Write-Host ""

# Run the Python app
python app.py

Write-Host ""
Write-Host "Application stopped." -ForegroundColor Red
Read-Host "Press Enter to exit"
