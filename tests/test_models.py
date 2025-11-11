"""
Model tests
"""
import pytest
from models import User, Review, ScrapeJob

def test_user_creation(db):
    """Test user model"""
    from werkzeug.security import generate_password_hash
    
    user = User(
        email='test@example.com',
        name='Test User',
        password_hash=generate_password_hash('password')
    )
    db.session.add(user)
    db.session.commit()
    
    assert user.id is not None
    assert user.email == 'test@example.com'

def test_review_creation(db):
    """Test review model"""
    review = Review(
        text='Great product!',
        sentiment='positive',
        emotion='happy',
        confidence=0.95
    )
    db.session.add(review)
    db.session.commit()
    
    assert review.id is not None
    assert review.sentiment == 'positive'

def test_scrape_job_creation(db):
    """Test scrape job model"""
    job = ScrapeJob(
        task_id='test-task-123',
        source='google_maps',
        url='https://example.com',
        status='pending'
    )
    db.session.add(job)
    db.session.commit()
    
    assert job.id is not None
    assert job.status == 'pending'
