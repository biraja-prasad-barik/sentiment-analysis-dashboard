# ============================================================================
# START SERVER - Fixed Version
# ============================================================================

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  STARTING SENTIMENT ANALYSIS SERVER" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Step 1: Stop old containers
Write-Host "[1/5] Stopping old containers..." -ForegroundColor Yellow
docker-compose down
Start-Sleep -Seconds 2

# Step 2: Remove old containers
Write-Host "`n[2/5] Cleaning up..." -ForegroundColor Yellow
docker-compose rm -f

# Step 3: Start services
Write-Host "`n[3/5] Starting all services..." -ForegroundColor Yellow
docker-compose up -d

# Step 4: Wait for services
Write-Host "`n[4/5] Waiting for services to be ready (40 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 40

# Step 5: Initialize database
Write-Host "`n[5/5] Initializing database..." -ForegroundColor Yellow
docker-compose exec web python scripts/init_db.py

# Check status
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  STATUS" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

docker-compose ps

# Test health
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  HEALTH CHECK" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

Start-Sleep -Seconds 5

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/v1/health" -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ Server is running!" -ForegroundColor Green
    Write-Host $response.Content -ForegroundColor Gray
} catch {
    Write-Host "⚠️  Server starting... (may take a few more seconds)" -ForegroundColor Yellow
}

# Final message
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  READY!" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

Write-Host "✅ Server started successfully!" -ForegroundColor Green
Write-Host "`n📍 Access your application at:" -ForegroundColor White
Write-Host "   http://localhost:5000" -ForegroundColor Cyan

Write-Host "`n🔐 Login credentials:" -ForegroundColor White
Write-Host "   Email: admin@sentiment.ai" -ForegroundColor Cyan
Write-Host "   Password: Admin123!" -ForegroundColor Cyan

Write-Host "`n📊 View logs:" -ForegroundColor White
Write-Host "   docker-compose logs -f web" -ForegroundColor Gray

Write-Host "`n🛑 Stop server:" -ForegroundColor White
Write-Host "   docker-compose down" -ForegroundColor Gray

Write-Host "`n🌐 Opening browser..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
start http://localhost:5000

Write-Host "`n"
