@echo off
echo ============================================
echo   SENTIMENT ANALYSIS - INSTALL AND RUN
echo ============================================
echo.

echo [1/3] Installing dependencies...
pip install flask flask-cors flask-sqlalchemy werkzeug

echo.
echo [2/3] Testing installation...
python test_setup.py

echo.
echo [3/3] Starting application...
echo.
echo ============================================
echo   Application starting...
echo   Open: http://localhost:5000
echo   Login: admin / admin123
echo ============================================
echo.

python app_simple.py

pause
