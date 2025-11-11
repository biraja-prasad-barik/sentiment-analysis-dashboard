"""
Main API routes
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from core.extensions import db, cache, limiter
from models import Review  # Import from models package
from services.sentiment_service import SentimentService
from utils.validators import validate_text_input
from utils.decorators import handle_errors
import logging

logger = logging.getLogger(__name__)
sentiment_service = SentimentService()

@api_bp.route('/analyze', methods=['POST'])
@limiter.limit("20 per minute")
@jwt_required(optional=True)
@handle_errors
def analyze_text():
    """Analyze sentiment of text"""
    data = request.get_json()
    
    # Validate input
    is_valid, error = validate_text_input(data)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    text = data.get('text')
    user_id = get_jwt_identity() if get_jwt_identity() else None
    
    # Check cache
    cache_key = f"sentiment:{hash(text)}"
    cached_result = cache.get(cache_key)
    if cached_result:
        logger.info(f"Cache hit for text analysis")
        return jsonify(cached_result)
    
    # Analyze
    result = sentiment_service.analyze(text)
    
    # Save to database
    review = Review(
        text=text,
        sentiment=result['sentiment'],
        emotion=result['emotion'],
        confidence=result['confidence'],
        user_id=user_id
    )
    db.session.add(review)
    db.session.commit()
    
    # Cache result
    cache.set(cache_key, result, timeout=3600)
    
    logger.info(f"Text analyzed - Sentiment: {result['sentiment']}, Emotion: {result['emotion']}")
    
    return jsonify(result), 200


@api_bp.route('/reviews', methods=['GET'])
@jwt_required(optional=True)
@cache.cached(timeout=60, query_string=True)
@handle_errors
def get_reviews():
    """Get paginated reviews"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    sentiment_filter = request.args.get('sentiment')
    emotion_filter = request.args.get('emotion')
    source_filter = request.args.get('source')
    
    # Build query
    query = Review.query
    
    if sentiment_filter:
        query = query.filter_by(sentiment=sentiment_filter)
    if emotion_filter:
        query = query.filter_by(emotion=emotion_filter)
    if source_filter:
        query = query.filter_by(source=source_filter)
    
    # Paginate
    reviews = query.order_by(Review.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'reviews': [{
            'id': r.id,
            'text': r.text,
            'sentiment': r.sentiment,
            'emotion': r.emotion,
            'confidence': r.confidence,
            'source': r.source,
            'created_at': r.created_at.isoformat()
        } for r in reviews.items],
        'total': reviews.total,
        'pages': reviews.pages,
        'current_page': page,
        'per_page': per_page
    }), 200


@api_bp.route('/reviews/<int:review_id>', methods=['GET'])
@jwt_required(optional=True)
@handle_errors
def get_review(review_id):
    """Get single review by ID"""
    review = Review.query.get_or_404(review_id)
    
    return jsonify({
        'id': review.id,
        'text': review.text,
        'sentiment': review.sentiment,
        'emotion': review.emotion,
        'confidence': review.confidence,
        'source': review.source,
        'created_at': review.created_at.isoformat()
    }), 200


@api_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
@handle_errors
def delete_review(review_id):
    """Delete a review"""
    review = Review.query.get_or_404(review_id)
    
    db.session.delete(review)
    db.session.commit()
    
    logger.info(f"Review {review_id} deleted")
    
    return jsonify({'message': 'Review deleted successfully'}), 200
