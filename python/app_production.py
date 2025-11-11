"""
Production-ready Flask application
"""
import os
from flask import Flask, render_template
from config import get_config
from core.extensions import init_extensions
from core.logging_config import setup_logging
from core.celery_app import init_celery
from core.monitoring import track_request, track_response
import logging

def create_app(config_name=None):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    config_class = get_config()
    app.config.from_object(config_class)
    
    # Setup logging
    setup_logging(app)
    logger = logging.getLogger(__name__)
    logger.info(f"Starting application in {config_name} mode")
    
    # Initialize extensions
    init_extensions(app)
    
    # Initialize Celery
    init_celery(app)
    
    # Register blueprints
    from api import api_bp
    app.register_blueprint(api_bp)
    
    # Request/response monitoring
    app.before_request(track_request)
    app.after_request(track_response)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(429)
    def ratelimit_handler(error):
        return {'error': 'Rate limit exceeded. Please try again later.'}, 429
    
    # Main route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Create database tables
    with app.app_context():
        from core.extensions import db
        db.create_all()
        logger.info("Database tables created")
    
    logger.info("Application initialized successfully")
    
    return app


# Create app instance
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
