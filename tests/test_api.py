"""
API endpoint tests
"""
import pytest

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_register_user(client):
    """Test user registration"""
    response = client.post('/api/v1/auth/register', json={
        'email': 'newuser@example.com',
        'name': 'New User',
        'password': 'SecurePass123'
    })
    assert response.status_code == 201
    assert 'access_token' in response.json

def test_login(client, sample_user):
    """Test user login"""
    response = client.post('/api/v1/auth/login', json={
        'email': 'test@example.com',
        'password': 'TestPass123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_analyze_text(client):
    """Test text analysis"""
    response = client.post('/api/v1/analyze', json={
        'text': 'This is a great product! I love it!'
    })
    assert response.status_code == 200
    assert 'sentiment' in response.json
    assert 'emotion' in response.json

def test_get_reviews(client, db):
    """Test getting reviews"""
    from models import Review
    
    # Create sample review
    review = Review(
        text='Test review',
        sentiment='positive',
        emotion='happy',
        confidence=0.95
    )
    db.session.add(review)
    db.session.commit()
    
    response = client.get('/api/v1/reviews')
    assert response.status_code == 200
    assert len(response.json['reviews']) > 0

def test_analytics_dashboard(client):
    """Test analytics endpoint"""
    response = client.get('/api/v1/analytics/dashboard')
    assert response.status_code == 200
    assert 'total_reviews' in response.json
    assert 'sentiment_distribution' in response.json
