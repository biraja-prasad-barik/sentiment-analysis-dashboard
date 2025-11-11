"""
Scrape Job model
"""
from datetime import datetime
from core.extensions import db

class ScrapeJob(db.Model):
    __tablename__ = 'scrape_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(100), unique=True, index=True)
    source = db.Column(db.String(50), nullable=False)
    url = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending', index=True)  # pending, processing, completed, failed
    reviews_count = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    reviews = db.relationship('Review', backref='scrape_job', lazy='dynamic')
    
    def __repr__(self):
        return f'<ScrapeJob {self.id} - {self.status}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'source': self.source,
            'url': self.url,
            'status': self.status,
            'reviews_count': self.reviews_count,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
