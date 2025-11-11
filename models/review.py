"""
Review model
"""
from datetime import datetime
from core.extensions import db

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20), nullable=False, index=True)
    emotion = db.Column(db.String(20), nullable=False, index=True)
    confidence = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(50), index=True)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    scrape_job_id = db.Column(db.Integer, db.ForeignKey('scrape_jobs.id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f'<Review {self.id} - {self.sentiment}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'text': self.text,
            'sentiment': self.sentiment,
            'emotion': self.emotion,
            'confidence': self.confidence,
            'source': self.source,
            'created_at': self.created_at.isoformat()
        }


class Analytics(db.Model):
    __tablename__ = 'analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True, index=True)
    total_reviews = db.Column(db.Integer, default=0)
    positive_count = db.Column(db.Integer, default=0)
    negative_count = db.Column(db.Integer, default=0)
    neutral_count = db.Column(db.Integer, default=0)
    avg_confidence = db.Column(db.Float, default=0.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Analytics {self.date}>'
