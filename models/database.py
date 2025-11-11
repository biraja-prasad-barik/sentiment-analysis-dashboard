from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20), nullable=False)
    emotion = db.Column(db.String(20), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(50), default='manual')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.id}: {self.sentiment}>'

class Analytics(db.Model):
    __tablename__ = 'analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    total_reviews = db.Column(db.Integer, default=0)
    positive_count = db.Column(db.Integer, default=0)
    negative_count = db.Column(db.Integer, default=0)
    neutral_count = db.Column(db.Integer, default=0)
    avg_confidence = db.Column(db.Float, default=0.0)
    
    def __repr__(self):
        return f'<Analytics {self.date}>'
