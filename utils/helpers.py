"""
Helper functions
"""
from datetime import datetime, timedelta
import hashlib
import secrets

def generate_api_key():
    """Generate a random API key"""
    return secrets.token_urlsafe(32)

def hash_text(text):
    """Generate hash of text for caching"""
    return hashlib.sha256(text.encode()).hexdigest()

def format_datetime(dt):
    """Format datetime for display"""
    if not dt:
        return None
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def calculate_date_range(days):
    """Calculate date range"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date

def paginate_query(query, page, per_page, max_per_page=100):
    """Helper for pagination"""
    per_page = min(per_page, max_per_page)
    return query.paginate(page=page, per_page=per_page, error_out=False)

def calculate_percentage(part, total):
    """Calculate percentage safely"""
    if total == 0:
        return 0.0
    return round((part / total) * 100, 2)
