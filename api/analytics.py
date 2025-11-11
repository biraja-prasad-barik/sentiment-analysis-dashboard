"""
Analytics endpoints
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from sqlalchemy import func
from . import api_bp
from core.extensions import db, cache
from models import Review  # Import from models package
from utils.decorators import handle_errors
import logging

logger = logging.getLogger(__name__)

@api_bp.route('/analytics/dashboard', methods=['GET'])
@jwt_required(optional=True)
@cache.cached(timeout=300, query_string=True)
@handle_errors
def get_dashboard_analytics():
    """Get dashboard analytics"""
    days = request.args.get('days', 7, type=int)
    days = min(days, 90)  # Max 90 days
    
    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get reviews in date range
    reviews = Review.query.filter(
        Review.created_at >= start_date
    ).all()
    
    # Calculate statistics
    total_reviews = len(reviews)
    
    sentiment_counts = {
        'positive': sum(1 for r in reviews if r.sentiment == 'positive'),
        'negative': sum(1 for r in reviews if r.sentiment == 'negative'),
        'neutral': sum(1 for r in reviews if r.sentiment == 'neutral')
    }
    
    emotion_counts = {}
    for review in reviews:
        emotion_counts[review.emotion] = emotion_counts.get(review.emotion, 0) + 1
    
    # Source distribution
    source_counts = {}
    for review in reviews:
        if review.source:
            source_counts[review.source] = source_counts.get(review.source, 0) + 1
    
    # Trend data
    trend_data = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        day_reviews = [r for r in reviews if r.created_at.date() == date.date()]
        
        trend_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'positive': sum(1 for r in day_reviews if r.sentiment == 'positive'),
            'negative': sum(1 for r in day_reviews if r.sentiment == 'negative'),
            'neutral': sum(1 for r in day_reviews if r.sentiment == 'neutral'),
            'total': len(day_reviews)
        })
    
    # Calculate satisfaction score
    satisfaction_score = (
        round((sentiment_counts['positive'] / total_reviews * 100), 2)
        if total_reviews > 0 else 0
    )
    
    # Average confidence
    avg_confidence = (
        round(sum(r.confidence for r in reviews) / total_reviews, 4)
        if total_reviews > 0 else 0
    )
    
    return jsonify({
        'total_reviews': total_reviews,
        'sentiment_distribution': sentiment_counts,
        'emotion_distribution': emotion_counts,
        'source_distribution': source_counts,
        'trend_data': trend_data,
        'satisfaction_score': satisfaction_score,
        'avg_confidence': avg_confidence,
        'date_range': {
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d'),
            'days': days
        }
    }), 200


@api_bp.route('/analytics/sentiment-trends', methods=['GET'])
@jwt_required(optional=True)
@cache.cached(timeout=300, query_string=True)
@handle_errors
def get_sentiment_trends():
    """Get detailed sentiment trends"""
    days = request.args.get('days', 30, type=int)
    source = request.args.get('source')
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    query = Review.query.filter(Review.created_at >= start_date)
    if source:
        query = query.filter_by(source=source)
    
    reviews = query.all()
    
    # Group by date
    trends = {}
    for review in reviews:
        date_key = review.created_at.strftime('%Y-%m-%d')
        if date_key not in trends:
            trends[date_key] = {
                'positive': 0, 'negative': 0, 'neutral': 0,
                'emotions': {}, 'avg_confidence': []
            }
        
        trends[date_key][review.sentiment] += 1
        trends[date_key]['emotions'][review.emotion] = \
            trends[date_key]['emotions'].get(review.emotion, 0) + 1
        trends[date_key]['avg_confidence'].append(review.confidence)
    
    # Format response
    result = []
    for date_key in sorted(trends.keys()):
        data = trends[date_key]
        total = data['positive'] + data['negative'] + data['neutral']
        
        result.append({
            'date': date_key,
            'positive': data['positive'],
            'negative': data['negative'],
            'neutral': data['neutral'],
            'total': total,
            'positive_pct': round(data['positive'] / total * 100, 2) if total > 0 else 0,
            'negative_pct': round(data['negative'] / total * 100, 2) if total > 0 else 0,
            'emotions': data['emotions'],
            'avg_confidence': round(
                sum(data['avg_confidence']) / len(data['avg_confidence']), 4
            ) if data['avg_confidence'] else 0
        })
    
    return jsonify({
        'trends': result,
        'summary': {
            'total_reviews': len(reviews),
            'date_range': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        }
    }), 200


@api_bp.route('/analytics/export', methods=['GET'])
@jwt_required()
@handle_errors
def export_analytics():
    """Export analytics data (CSV format)"""
    from io import StringIO
    import csv
    
    days = request.args.get('days', 30, type=int)
    format_type = request.args.get('format', 'csv')
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    reviews = Review.query.filter(
        Review.created_at >= start_date
    ).all()
    
    if format_type == 'csv':
        output = StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            'ID', 'Date', 'Text', 'Sentiment', 'Emotion',
            'Confidence', 'Source'
        ])
        
        # Data
        for review in reviews:
            writer.writerow([
                review.id,
                review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                review.text,
                review.sentiment,
                review.emotion,
                review.confidence,
                review.source or 'manual'
            ])
        
        output.seek(0)
        
        from flask import Response
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename=analytics_{start_date.strftime("%Y%m%d")}.csv'
            }
        )
    
    return jsonify({'error': 'Unsupported format'}), 400


@api_bp.route('/analytics/comparison', methods=['GET'])
@jwt_required(optional=True)
@cache.cached(timeout=300, query_string=True)
@handle_errors
def compare_sources():
    """Compare sentiment across different sources"""
    days = request.args.get('days', 30, type=int)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    reviews = Review.query.filter(
        Review.created_at >= start_date,
        Review.source.isnot(None)
    ).all()
    
    # Group by source
    sources = {}
    for review in reviews:
        if review.source not in sources:
            sources[review.source] = {
                'positive': 0, 'negative': 0, 'neutral': 0,
                'total': 0, 'avg_confidence': []
            }
        
        sources[review.source][review.sentiment] += 1
        sources[review.source]['total'] += 1
        sources[review.source]['avg_confidence'].append(review.confidence)
    
    # Format response
    comparison = []
    for source, data in sources.items():
        total = data['total']
        comparison.append({
            'source': source,
            'total_reviews': total,
            'positive': data['positive'],
            'negative': data['negative'],
            'neutral': data['neutral'],
            'positive_pct': round(data['positive'] / total * 100, 2),
            'negative_pct': round(data['negative'] / total * 100, 2),
            'satisfaction_score': round(data['positive'] / total * 100, 2),
            'avg_confidence': round(
                sum(data['avg_confidence']) / len(data['avg_confidence']), 4
            )
        })
    
    # Sort by total reviews
    comparison.sort(key=lambda x: x['total_reviews'], reverse=True)
    
    return jsonify({
        'comparison': comparison,
        'total_sources': len(comparison),
        'date_range': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    }), 200
