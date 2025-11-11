"""
Development Configuration
Simple configuration for local development

To use different settings, modify this file or set environment variables.
"""

import os


class DevelopmentConfig:
    """Development configuration"""
    
    # Flask settings
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Server settings
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///sentiment_dev.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True to see SQL queries
    
    # Scraping settings
    SCRAPING_MAX_REVIEWS = 50
    SCRAPING_TIMEOUT = 15  # seconds
    SCRAPING_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    SCRAPING_RESPECT_ROBOTS_TXT = True
    
    # Analysis settings
    MIN_TEXT_LENGTH = 5
    MAX_TEXT_LENGTH = 5000
    DEFAULT_CONFIDENCE_THRESHOLD = 0.5
    
    # Pagination settings
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # CORS settings
    CORS_ORIGINS = '*'  # Allow all origins in development
    
    # Logging settings
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class TestingConfig(DevelopmentConfig):
    """Testing configuration"""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False


class ProductionConfig:
    """
    Production configuration (not used in development version)
    
    These settings will be used when production features are added:
    - PostgreSQL database
    - Redis for caching
    - Celery for background tasks
    - Proper secret key management
    - HTTPS/SSL
    - Rate limiting
    - etc.
    """
    
    DEBUG = False
    TESTING = False
    
    # These would be set via environment variables in production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    REDIS_URL = os.environ.get('REDIS_URL')
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    
    # Production-specific settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
