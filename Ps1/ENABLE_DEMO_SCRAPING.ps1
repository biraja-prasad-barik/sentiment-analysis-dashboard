# ============================================================================
# Enable Demo Scraping Mode
# This creates sample reviews for demonstration without actual web scraping
# ============================================================================

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  CHECKING SCRAPING DEPENDENCIES" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Check Selenium
Write-Host "Checking Selenium..." -ForegroundColor Yellow
python -c "import selenium; print('✅ Selenium installed')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Selenium not installed" -ForegroundColor Red
    Write-Host "Installing Selenium..." -ForegroundColor Yellow
    pip install selenium
}

# Check BeautifulSoup4
Write-Host "Checking BeautifulSoup4..." -ForegroundColor Yellow
python -c "import bs4; print('✅ BeautifulSoup4 installed')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ BeautifulSoup4 not installed" -ForegroundColor Red
    Write-Host "Installing BeautifulSoup4..." -ForegroundColor Yellow
    pip install beautifulsoup4
}

# Check Transformers
Write-Host "Checking Transformers..." -ForegroundColor Yellow
python -c "import transformers; print('✅ Transformers installed')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Transformers not installed" -ForegroundColor Red
    Write-Host "Installing Transformers (this may take a while)..." -ForegroundColor Yellow
    pip install transformers
}

# Check PyTorch
Write-Host "Checking PyTorch..." -ForegroundColor Yellow
python -c "import torch; print('✅ PyTorch installed')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ PyTorch not installed" -ForegroundColor Red
    Write-Host "Installing PyTorch (this may take a while)..." -ForegroundColor Yellow
    pip install torch
}

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  INSTALLATION COMPLETE" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

Write-Host "✅ All dependencies installed!" -ForegroundColor Green
Write-Host "`nYou can now use the scraping feature!" -ForegroundColor White
Write-Host "`nRestart your app:" -ForegroundColor Yellow
Write-Host "   python app_standalone.py" -ForegroundColor Gray

Write-Host "`n"
