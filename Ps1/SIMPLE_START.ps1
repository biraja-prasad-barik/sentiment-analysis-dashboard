# ============================================================================
# SIMPLE START - No Database Init Needed
# ============================================================================

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  STARTING SERVER" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

cd "C:\Users\kbari\OneDrive\Desktop\Sentiment Analyzer Project"

# Stop old containers
Write-Host "Stopping old containers..." -ForegroundColor Yellow
docker-compose down

# Start services
Write-Host "Starting services..." -ForegroundColor Yellow
docker-compose up -d

# Wait
Write-Host "Waiting for services (30 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check status
Write-Host "`nChecking status..." -ForegroundColor Yellow
docker-compose ps

# Test connection
Write-Host "`nTesting connection..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ Server is running!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Server may still be starting..." -ForegroundColor Yellow
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Gray
}

# Show logs
Write-Host "`nRecent logs:" -ForegroundColor Yellow
docker-compose logs --tail=20 web

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  READY!" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

Write-Host "📍 Open: http://localhost:5000" -ForegroundColor Cyan
Write-Host "`nIf you see a login page, try:" -ForegroundColor White
Write-Host "   Email: admin@sentiment.ai" -ForegroundColor Gray
Write-Host "   Password: Admin123!" -ForegroundColor Gray

Write-Host "`nOpening browser..." -ForegroundColor Yellow
start http://localhost:5000

Write-Host "`n"
