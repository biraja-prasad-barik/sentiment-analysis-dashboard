# ============================================================================
# Docker Fix and Start Script
# Run this in PowerShell to fix and start all services
# ============================================================================

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  DOCKER FIX AND START" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Step 1: Stop all containers
Write-Host "[1/6] Stopping all containers..." -ForegroundColor Yellow
docker-compose down
Start-Sleep -Seconds 2

# Step 2: Start postgres only
Write-Host "`n[2/6] Starting PostgreSQL..." -ForegroundColor Yellow
docker-compose up -d postgres
Write-Host "Waiting for PostgreSQL to be ready..." -ForegroundColor Gray
Start-Sleep -Seconds 10

# Step 3: Rebuild images
Write-Host "`n[3/6] Rebuilding Docker images..." -ForegroundColor Yellow
docker-compose build --no-cache web celery_worker celery_beat

# Step 4: Start all services
Write-Host "`n[4/6] Starting all services..." -ForegroundColor Yellow
docker-compose up -d

# Step 5: Wait for services to be healthy
Write-Host "`n[5/6] Waiting for services to be healthy (30 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Step 6: Initialize database
Write-Host "`n[6/6] Initializing database..." -ForegroundColor Yellow
docker-compose exec web python scripts/init_db.py

# Check status
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  STATUS CHECK" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

docker-compose ps

# Test health endpoint
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  HEALTH CHECK" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/v1/health" -UseBasicParsing
    Write-Host "✅ Health check passed!" -ForegroundColor Green
    Write-Host $response.Content -ForegroundColor Gray
} catch {
    Write-Host "❌ Health check failed!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
}

# Show logs
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  RECENT LOGS" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

docker-compose logs --tail=20 web

# Final message
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  DONE!" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

Write-Host "✅ Services started!" -ForegroundColor Green
Write-Host "`nAccess your application at:" -ForegroundColor White
Write-Host "  http://localhost:5000" -ForegroundColor Cyan
Write-Host "`nLogin credentials:" -ForegroundColor White
Write-Host "  Email: admin@sentiment.ai" -ForegroundColor Cyan
Write-Host "  Password: Admin123!" -ForegroundColor Cyan

Write-Host "`nTo view logs:" -ForegroundColor White
Write-Host "  docker-compose logs -f web" -ForegroundColor Gray

Write-Host "`nTo stop services:" -ForegroundColor White
Write-Host "  docker-compose down" -ForegroundColor Gray

Write-Host "`n"
