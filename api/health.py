"""
Health check and monitoring endpoints
"""
from flask import jsonify
from . import api_bp
from core.extensions import db
from core.monitoring import get_metrics
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Basic health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'sentiment-analysis-api'
    }), 200


@api_bp.route('/health/detailed', methods=['GET'])
def detailed_health_check():
    """Detailed health check with dependencies"""
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'checks': {}
    }
    
    # Check database
    try:
        db.session.execute('SELECT 1')
        health_status['checks']['database'] = {
            'status': 'healthy',
            'message': 'Database connection OK'
        }
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['database'] = {
            'status': 'unhealthy',
            'message': str(e)
        }
        logger.error(f"Database health check failed: {e}")
    
    # Check Redis (cache)
    try:
        from core.extensions import cache
        cache.set('health_check', 'ok', timeout=10)
        if cache.get('health_check') == 'ok':
            health_status['checks']['cache'] = {
                'status': 'healthy',
                'message': 'Cache connection OK'
            }
        else:
            raise Exception("Cache read/write failed")
    except Exception as e:
        health_status['checks']['cache'] = {
            'status': 'degraded',
            'message': f'Cache unavailable: {str(e)}'
        }
        logger.warning(f"Cache health check failed: {e}")
    
    # Check Celery
    try:
        from core.celery_app import celery
        inspect = celery.control.inspect()
        stats = inspect.stats()
        if stats:
            health_status['checks']['celery'] = {
                'status': 'healthy',
                'message': 'Celery workers active',
                'workers': len(stats)
            }
        else:
            health_status['checks']['celery'] = {
                'status': 'degraded',
                'message': 'No Celery workers found'
            }
    except Exception as e:
        health_status['checks']['celery'] = {
            'status': 'degraded',
            'message': f'Celery unavailable: {str(e)}'
        }
        logger.warning(f"Celery health check failed: {e}")
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code


@api_bp.route('/metrics', methods=['GET'])
def get_app_metrics():
    """Get application metrics"""
    metrics = get_metrics()
    
    # Add database metrics
    try:
        from models import Review, User
        metrics['database'] = {
            'total_reviews': Review.query.count(),
            'total_users': User.query.count()
        }
    except Exception as e:
        logger.warning(f"Could not get database metrics: {e}")
        pass
    
    return jsonify(metrics), 200


@api_bp.route('/version', methods=['GET'])
def get_version():
    """Get API version info"""
    return jsonify({
        'version': '1.0.0',
        'api_version': 'v1',
        'environment': 'production',
        'build_date': '2024-01-01'
    }), 200
