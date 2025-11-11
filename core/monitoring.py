"""
Monitoring and metrics
"""
import time
from functools import wraps
from flask import request, g
import logging

logger = logging.getLogger(__name__)

# Simple in-memory metrics (use Prometheus in production)
metrics = {
    'requests_total': 0,
    'requests_by_endpoint': {},
    'response_times': [],
    'errors_total': 0,
}

def track_request():
    """Track request metrics"""
    g.start_time = time.time()
    metrics['requests_total'] += 1
    
def track_response(response):
    """Track response metrics"""
    if hasattr(g, 'start_time'):
        response_time = time.time() - g.start_time
        metrics['response_times'].append(response_time)
        
        # Keep only last 1000 response times
        if len(metrics['response_times']) > 1000:
            metrics['response_times'] = metrics['response_times'][-1000:]
        
        endpoint = request.endpoint or 'unknown'
        if endpoint not in metrics['requests_by_endpoint']:
            metrics['requests_by_endpoint'][endpoint] = 0
        metrics['requests_by_endpoint'][endpoint] += 1
        
        if response.status_code >= 400:
            metrics['errors_total'] += 1
    
    return response

def get_metrics():
    """Get current metrics"""
    avg_response_time = (
        sum(metrics['response_times']) / len(metrics['response_times'])
        if metrics['response_times'] else 0
    )
    
    return {
        'requests_total': metrics['requests_total'],
        'errors_total': metrics['errors_total'],
        'avg_response_time_ms': round(avg_response_time * 1000, 2),
        'requests_by_endpoint': metrics['requests_by_endpoint'],
    }

def monitor_performance(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start
            logger.info(f"{func.__name__} completed in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start
            logger.error(f"{func.__name__} failed after {duration:.2f}s: {str(e)}")
            raise
    return wrapper
