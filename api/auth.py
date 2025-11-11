"""
Authentication endpoints
"""
from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
from . import api_bp
from core.extensions import db, limiter
from models import User  # Import from models package
from utils.validators import validate_email, validate_password
from utils.decorators import handle_errors
import logging

logger = logging.getLogger(__name__)

@api_bp.route('/auth/register', methods=['POST'])
@limiter.limit("5 per hour")
@handle_errors
def register():
    """Register new user"""
    data = request.get_json()
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    name = data.get('name', '').strip()
    
    # Validate
    if not validate_email(email):
        return jsonify({'error': 'Invalid email address'}), 400
    
    is_valid, error = validate_password(password)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    if not name or len(name) < 2:
        return jsonify({'error': 'Name must be at least 2 characters'}), 400
    
    # Check if user exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create user
    user = User(
        email=email,
        name=name,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()
    
    logger.info(f"New user registered: {email}")
    
    # Generate tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name
        }
    }), 201


@api_bp.route('/auth/login', methods=['POST'])
@limiter.limit("10 per minute")
@handle_errors
def login():
    """Login user"""
    data = request.get_json()
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    # Find user
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        logger.warning(f"Failed login attempt for: {email}")
        return jsonify({'error': 'Invalid email or password'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is disabled'}), 403
    
    # Update last login
    user.update_last_login()
    db.session.commit()
    
    logger.info(f"User logged in: {email}")
    
    # Generate tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role
        }
    }), 200


@api_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
@handle_errors
def refresh():
    """Refresh access token"""
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    
    return jsonify({'access_token': access_token}), 200


@api_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
@handle_errors
def logout():
    """Logout user (client should delete tokens)"""
    user_id = get_jwt_identity()
    logger.info(f"User logged out: {user_id}")
    
    return jsonify({'message': 'Logged out successfully'}), 200


@api_bp.route('/auth/me', methods=['GET'])
@jwt_required()
@handle_errors
def get_current_user():
    """Get current user info"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'role': user.role,
        'is_active': user.is_active,
        'created_at': user.created_at.isoformat()
    }), 200


@api_bp.route('/auth/change-password', methods=['POST'])
@jwt_required()
@handle_errors
def change_password():
    """Change user password"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    data = request.get_json()
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')
    
    # Verify old password
    if not check_password_hash(user.password_hash, old_password):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    # Validate new password
    is_valid, error = validate_password(new_password)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    # Update password
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    logger.info(f"Password changed for user: {user.email}")
    
    return jsonify({'message': 'Password changed successfully'}), 200
