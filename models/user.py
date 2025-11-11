"""
User model
"""
from datetime import datetime
from core.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, admin
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    scrape_jobs = db.relationship('ScrapeJob', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
