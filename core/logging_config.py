"""
Logging configuration
"""
import logging
import os
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
            
        return json.dumps(log_data)


def setup_logging(app):
    """Setup application logging"""
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(app.config['LOG_FILE'])
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Set log level
    log_level = getattr(logging, app.config['LOG_LEVEL'].upper())
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        app.config['LOG_FILE'],
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(JsonFormatter())
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Configure app logger
    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    
    # Configure werkzeug logger
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.WARNING)
    werkzeug_logger.addHandler(file_handler)
    
    app.logger.info(f"Logging initialized - Level: {app.config['LOG_LEVEL']}")
