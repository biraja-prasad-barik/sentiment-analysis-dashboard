"""
Pytest configuration and fixtures
"""
import pytest
from app_production import create_app
from core.extensions import db as _db
from models import User, Review

@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture(scope='function')
def db(app):
    """Create database for testing"""
    with app.app_context():
        _db.session.begin_nested()
        yield _db
        _db.session.rollback()

@pytest.fixture
def sample_user(db):
    """Create sample user"""
    from werkzeug.security import generate_password_hash
    
    user = User(
        email='test@example.com',
        name='Test User',
        password_hash=generate_password_hash('TestPass123')
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def auth_headers(client, sample_user):
    """Get authentication headers"""
    response = client.post('/api/v1/auth/login', json={
        'email': 'test@example.com',
        'password': 'TestPass123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}
