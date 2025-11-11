"""
Scraping endpoints with async support
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from core.extensions import limiter
from tasks.scraping_tasks import scrape_reviews_task
from utils.validators import validate_url
from utils.decorators import handle_errors
import logging

logger = logging.getLogger(__name__)

@api_bp.route('/scrape', methods=['POST'])
@limiter.limit("5 per hour")
@jwt_required(optional=True)
@handle_errors
def scrape_reviews():
    """Initiate async scraping task"""
    data = request.get_json()
    
    source = data.get('source')
    url = data.get('url')
    max_reviews = data.get('max_reviews', 100)
    
    # Validate
    if not source or not url:
        return jsonify({'error': 'Source and URL required'}), 400
    
    if not validate_url(url):
        return jsonify({'error': 'Invalid URL'}), 400
    
    valid_sources = ['google_maps', 'tripadvisor', 'yelp', 'amazon', 'hotel', 'generic']
    if source not in valid_sources:
        return jsonify({'error': f'Invalid source. Must be one of: {", ".join(valid_sources)}'}), 400
    
    max_reviews = min(max_reviews, 200)  # Limit to 200
    
    user_id = get_jwt_identity() if get_jwt_identity() else None
    
    # Start async task
    task = scrape_reviews_task.delay(source, url, max_reviews, user_id)
    
    logger.info(f"Scraping task started: {task.id} for {source} - {url}")
    
    return jsonify({
        'message': 'Scraping task started',
        'task_id': task.id,
        'status': 'pending',
        'estimated_time': '30-120 seconds'
    }), 202


@api_bp.route('/scrape/status/<task_id>', methods=['GET'])
@jwt_required(optional=True)
@handle_errors
def get_scrape_status(task_id):
    """Get status of scraping task"""
    from core.celery_app import celery
    
    task = celery.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        response = {
            'task_id': task_id,
            'status': 'pending',
            'message': 'Task is waiting to be processed'
        }
    elif task.state == 'STARTED':
        response = {
            'task_id': task_id,
            'status': 'processing',
            'message': 'Scraping in progress...'
        }
    elif task.state == 'SUCCESS':
        response = {
            'task_id': task_id,
            'status': 'completed',
            'result': task.result
        }
    elif task.state == 'FAILURE':
        response = {
            'task_id': task_id,
            'status': 'failed',
            'error': str(task.info)
        }
    else:
        response = {
            'task_id': task_id,
            'status': task.state.lower(),
            'message': 'Task status unknown'
        }
    
    return jsonify(response), 200


@api_bp.route('/scrape/history', methods=['GET'])
@jwt_required()
@handle_errors
def get_scrape_history():
    """Get user's scraping history"""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    from models import ScrapeJob
    
    jobs = ScrapeJob.query.filter_by(user_id=user_id).order_by(
        ScrapeJob.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'jobs': [{
            'id': job.id,
            'source': job.source,
            'url': job.url,
            'status': job.status,
            'reviews_count': job.reviews_count,
            'created_at': job.created_at.isoformat(),
            'completed_at': job.completed_at.isoformat() if job.completed_at else None
        } for job in jobs.items],
        'total': jobs.total,
        'pages': jobs.pages,
        'current_page': page
    }), 200
