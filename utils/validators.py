"""
Input validation utilities
"""
import re
from urllib.parse import urlparse

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Validate password strength
    Returns: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, None

def validate_url(url):
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def validate_text_input(data):
    """
    Validate text input for analysis
    Returns: (is_valid, error_message)
    """
    if not data:
        return False, "No data provided"
    
    text = data.get('text', '').strip()
    
    if not text:
        return False, "Text field is required"
    
    if len(text) < 10:
        return False, "Text must be at least 10 characters long"
    
    if len(text) > 5000:
        return False, "Text must not exceed 5000 characters"
    
    return True, None

def sanitize_input(text):
    """Sanitize user input"""
    # Remove potential XSS
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<.*?>', '', text)
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    return text.strip()
