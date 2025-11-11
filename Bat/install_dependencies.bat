@echo off
echo Installing dependencies for Sentiment Analysis App...
echo.

pip install flask==3.0.0
pip install flask-cors==4.0.0
pip install flask-sqlalchemy==3.1.1
pip install transformers==4.35.0
pip install torch==2.1.0
pip install numpy==1.24.3
pip install pandas==2.1.3
pip install scikit-learn==1.3.2
pip install beautifulsoup4==4.12.2
pip install requests==2.31.0
pip install python-dotenv==1.0.0

echo.
echo Optional: Installing Selenium for advanced scraping...
pip install selenium==4.15.0

echo.
echo Installation complete!
echo Run 'python app.py' to start the application.
pause
