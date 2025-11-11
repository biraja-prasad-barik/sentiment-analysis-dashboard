# ============================================================================
# Diagnose Container Issues
# ============================================================================

Write-Host "`n=== DIAGNOSING CONTAINER ISSUES ===" -ForegroundColor Cyan

cd "C:\Users\kbari\OneDrive\Desktop\Sentiment Analyzer Project"

# Check container status
Write-Host "`n[1] Container Status:" -ForegroundColor Yellow
docker-compose ps

# Check web container logs
Write-Host "`n[2] Web Container Logs (Last 50 lines):" -ForegroundColor Yellow
docker-compose logs --tail=50 web

# Check if container is restarting
Write-Host "`n[3] Container Restart Count:" -ForegroundColor Yellow
docker inspect sentiment_web --format='{{.RestartCount}}'

# Check container state
Write-Host "`n[4] Container State:" -ForegroundColor Yellow
docker inspect sentiment_web --format='{{.State.Status}}'

# Check what's inside container
Write-Host "`n[5] Files in Container:" -ForegroundColor Yellow
docker exec sentiment_web ls -la /app 2>&1

# Check if app_production.py exists
Write-Host "`n[6] Checking app_production.py:" -ForegroundColor Yellow
docker exec sentiment_web ls -la /app/app_production.py 2>&1

# Try to import the app
Write-Host "`n[7] Testing App Import:" -ForegroundColor Yellow
docker exec sentiment_web python -c "from app_production import app; print('✅ App import successful')" 2>&1

Write-Host "`n=== DIAGNOSIS COMPLETE ===" -ForegroundColor Cyan
Write-Host "`nIf you see errors above, that's the problem!" -ForegroundColor Yellow
