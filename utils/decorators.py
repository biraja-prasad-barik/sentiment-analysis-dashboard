"""
Custom decorators
"""
from functools import wraps
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def handle_errors(f):
    """Error handling decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation error in {f.__name__}: {e}")
            return jsonify({'error': str(e)}), 400
        except PermissionError as e:
            logger.warning(f"Permission error in {f.__name__}: {e}")
            return jsonify({'error': 'Permission denied'}), 403
        except FileNotFoundError as e:
            logger.warning(f"Not found error in {f.__name__}: {e}")
            return jsonify({'error': 'Resource not found'}), 404
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {e}", exc_info=True)
            return jsonify({'error': 'Internal server error'}), 500
    
    return decorated_function

def admin_required(f):
    """Require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask_jwt_extended import get_jwt_identity
        try:
            from models import User
        except ImportError:
            return jsonify({'error': 'User model not available'}), 500
        
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function
