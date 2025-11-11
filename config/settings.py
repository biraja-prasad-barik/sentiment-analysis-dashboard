"""
Configuration settings for different environments
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # App
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    APP_NAME = 'Sentiment Analysis Platform'
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Celery
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = REDIS_URL
    RATELIMIT_DEFAULT = "100 per hour"
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Scraping
    MAX_REVIEWS_PER_SCRAPE = 100
    SCRAPE_TIMEOUT = 300  # 5 minutes
    USE_PROXY = os.getenv('USE_PROXY', 'false').lower() == 'true'
    PROXY_LIST = os.getenv('PROXY_LIST', '').split(',') if os.getenv('PROXY_LIST') else []
    
    # ML Models
    MODEL_CACHE_DIR = os.getenv('MODEL_CACHE_DIR', './models/cache')
    USE_GPU = os.getenv('USE_GPU', 'false').lower() == 'true'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    # Monitoring
    SENTRY_DSN = os.getenv('SENTRY_DSN', '')
    ENABLE_METRICS = os.getenv('ENABLE_METRICS', 'true').lower() == 'true'
    
    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@sentiment.ai')
    
    # Pagination
    ITEMS_PER_PAGE = 20
    MAX_ITEMS_PER_PAGE = 100


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///dev_sentiment.db')
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_sentiment.db'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@localhost:5432/sentiment_prod'
    )
    # Force HTTPS
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Security headers
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
    }


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
