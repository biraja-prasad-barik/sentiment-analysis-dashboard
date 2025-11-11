"""
Initialize database with sample data
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_production import create_app
from core.extensions import db
from models import User, Review
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def init_database():
    """Initialize database with sample data"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Create admin user
        admin = User.query.filter_by(email='admin@sentiment.ai').first()
        if not admin:
            admin = User(
                email='admin@sentiment.ai',
                name='Admin User',
                password_hash=generate_password_hash('Admin123!'),
                role='admin'
            )
            db.session.add(admin)
            print("✅ Admin user created: admin@sentiment.ai / Admin123!")
        
        # Create sample user
        user = User.query.filter_by(email='demo@sentiment.ai').first()
        if not user:
            user = User(
                email='demo@sentiment.ai',
                name='Demo User',
                password_hash=generate_password_hash('Demo123!')
            )
            db.session.add(user)
            print("✅ Demo user created: demo@sentiment.ai / Demo123!")
        
        db.session.commit()
        
        # Create sample reviews
        if Review.query.count() == 0:
            print("Creating sample reviews...")
            
            sample_reviews = [
                ("This product is absolutely amazing! Best purchase ever!", "positive", "happy"),
                ("Terrible experience. Would not recommend to anyone.", "negative", "angry"),
                ("It's okay, nothing special but does the job.", "neutral", "satisfied"),
                ("I love this! Exceeded all my expectations!", "positive", "happy"),
                ("Worst service I've ever experienced. Very disappointed.", "negative", "sad"),
                ("Pretty good overall, happy with my purchase.", "positive", "satisfied"),
                ("Not what I expected, quite disappointing.", "negative", "sad"),
                ("Excellent quality and fast shipping!", "positive", "happy"),
                ("Average product, nothing to write home about.", "neutral", "satisfied"),
                ("Absolutely horrible! Waste of money!", "negative", "angry"),
            ]
            
            for i, (text, sentiment, emotion) in enumerate(sample_reviews):
                review = Review(
                    text=text,
                    sentiment=sentiment,
                    emotion=emotion,
                    confidence=random.uniform(0.7, 0.99),
                    source='sample_data',
                    user_id=user.id,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
                )
                db.session.add(review)
            
            db.session.commit()
            print(f"✅ Created {len(sample_reviews)} sample reviews")
        
        print("\n✅ Database initialized successfully!")
        print("\nLogin credentials:")
        print("  Admin: admin@sentiment.ai / Admin123!")
        print("  Demo:  demo@sentiment.ai / Demo123!")

if __name__ == '__main__':
    init_database()
