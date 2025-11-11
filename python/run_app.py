"""
Alternative startup script for Sentiment Analysis Web App
Use this if you want a cleaner startup with suppressed warnings
"""

import warnings
import os

# Suppress warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

print("\n" + "="*60)
print("🚀 SENTIMENT ANALYSIS WEB APPLICATION")
print("="*60)
print("\n📦 Loading dependencies...")

try:
    # Import Flask app
    from app import app, db
    
    print("✅ Dependencies loaded!")
    print("\n🔧 Initializing database...")
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database initialized!")
    
    print("\n" + "="*60)
    print("🎉 APPLICATION READY!")
    print("="*60)
    print("\n📍 Open your browser and go to:")
    print("\n   👉 http://localhost:5000")
    print("\n💡 Features:")
    print("   • Scrape reviews from Google Maps, TripAdvisor, Yelp, Amazon")
    print("   • AI-powered sentiment analysis using BERT")
    print("   • Real-time analytics dashboard")
    print("\n🛑 Press CTRL+C to stop the server")
    print("\n" + "="*60 + "\n")
    
    # Run the app
    app.run(debug=True, port=5000, use_reloader=False)
    
except ImportError as e:
    print(f"\n❌ ERROR: Missing dependencies!")
    print(f"   {str(e)}")
    print("\n💡 Solution: Run this command:")
    print("   pip install -r requirements.txt")
    print("\n")
    input("Press Enter to exit...")
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\n")
    input("Press Enter to exit...")
