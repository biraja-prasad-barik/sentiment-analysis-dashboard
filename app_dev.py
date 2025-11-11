#!/usr/bin/env python3
"""
Sentiment Analysis Dashboard - Development Version
Simple, stable, single-file Flask application

Run with: python app_dev.py
Open: http://localhost:5000

Note: Production features (Docker, Celery, etc.) intentionally removed.
They will be added later when requested.
"""

import os
import re
import logging
import hashlib
from datetime import datetime
from urllib.parse import urlparse
from functools import wraps
from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Simple configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentiment_dev.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Initialize database
db = SQLAlchemy(app)

# ============================================================================
# DATABASE MODELS
# ============================================================================

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def check_password(self, password):
        """Check if password matches"""
        return self.password_hash == hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Review(db.Model):
    """Review model for storing scraped reviews"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20), nullable=False)
    emotion = db.Column(db.String(20), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(100))
    url = db.Column(db.String(500))
    text_hash = db.Column(db.String(64), unique=True, index=True)  # For deduplication
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'sentiment': self.sentiment,
            'emotion': self.emotion,
            'confidence': round(self.confidence, 3),
            'source': self.source,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ============================================================================
# LIGHTWEIGHT ML MODEL (Keyword-Based)
# ============================================================================

class SimpleSentimentAnalyzer:
    """Lightweight sentiment analyzer using keyword-based approach"""
    
    def __init__(self):
        # Positive keywords
        self.positive_words = {
            'excellent', 'amazing', 'great', 'fantastic', 'wonderful', 'awesome',
            'love', 'perfect', 'best', 'outstanding', 'brilliant', 'superb',
            'good', 'nice', 'happy', 'satisfied', 'pleased', 'recommend',
            'beautiful', 'incredible', 'exceptional', 'delightful', 'impressive'
        }
        
        # Negative keywords
        self.negative_words = {
            'terrible', 'awful', 'horrible', 'bad', 'worst', 'hate', 'disgusting',
            'disappointing', 'poor', 'useless', 'broken', 'failed', 'wrong',
            'angry', 'frustrated', 'annoyed', 'upset', 'dissatisfied', 'waste',
            'pathetic', 'ridiculous', 'unacceptable', 'nightmare'
        }
        
        # Emotion keywords
        self.emotion_keywords = {
            'happy': {'happy', 'joy', 'excited', 'delighted', 'cheerful', 'pleased', 'thrilled'},
            'sad': {'sad', 'disappointed', 'depressed', 'unhappy', 'upset', 'miserable'},
            'angry': {'angry', 'furious', 'mad', 'irritated', 'annoyed', 'outraged'},
            'surprised': {'surprised', 'shocked', 'amazed', 'astonished', 'stunned'},
            'fear': {'scared', 'afraid', 'worried', 'nervous', 'anxious', 'terrified'},
            'love': {'love', 'adore', 'cherish', 'treasure', 'passionate'}
        }
    
    def preprocess_text(self, text):
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def analyze(self, text):
        """Analyze sentiment and emotion of text"""
        if not text or len(text.strip()) < 5:
            return {
                'sentiment': 'neutral',
                'emotion': 'neutral',
                'confidence': 0.5
            }
        
        # Preprocess
        text_clean = self.preprocess_text(text)
        words = set(text_clean.split())
        
        # Count positive and negative words
        positive_count = len(words.intersection(self.positive_words))
        negative_count = len(words.intersection(self.negative_words))
        
        # Determine sentiment
        if positive_count > negative_count:
            sentiment = 'positive'
            confidence = min(0.95, 0.6 + (positive_count - negative_count) * 0.1)
        elif negative_count > positive_count:
            sentiment = 'negative'
            confidence = min(0.95, 0.6 + (negative_count - positive_count) * 0.1)
        else:
            sentiment = 'neutral'
            confidence = 0.5
        
        # Determine emotion
        emotion_scores = {}
        for emotion, keywords in self.emotion_keywords.items():
            score = len(words.intersection(keywords))
            if score > 0:
                emotion_scores[emotion] = score
        
        if emotion_scores:
            emotion = max(emotion_scores, key=emotion_scores.get)
        else:
            emotion = 'neutral'
        
        return {
            'sentiment': sentiment,
            'emotion': emotion,
            'confidence': confidence
        }

# ============================================================================
# SIMPLE WEB SCRAPER
# ============================================================================

class SimpleReviewScraper:
    """Simple web scraper for extracting text content"""
    
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    
    def check_robots_txt(self, url):
        """Check if scraping is allowed by robots.txt"""
        try:
            from urllib.robotparser import RobotFileParser
            
            parsed = urlparse(url)
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
            
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            
            return rp.can_fetch(self.user_agent, url)
        except Exception as e:
            logger.warning(f"Could not check robots.txt: {e}")
            return True  # Allow if we can't check
    
    def scrape_reviews(self, url, max_reviews=10):
        """Extract text content from URL"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            # Check robots.txt
            if not self.check_robots_txt(url):
                logger.warning(f"Scraping not allowed by robots.txt: {url}")
                return []
            
            logger.info(f"Scraping reviews from: {url}")
            
            # Simple HTTP request
            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract text content
            reviews = []
            
            # Look for common review patterns
            review_selectors = [
                '.review-text', '.review-content', '.comment-text', '.review-body',
                '[data-review]', '.user-review', '.feedback-text', '.customer-review',
                'article', '.post-content', '.entry-content'
            ]
            
            for selector in review_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(strip=True)
                    # Filter reasonable length (20-2000 chars)
                    if 20 <= len(text) <= 2000:
                        reviews.append(text)
                        if len(reviews) >= max_reviews:
                            break
                if len(reviews) >= max_reviews:
                    break
            
            # If no reviews found with selectors, try paragraphs
            if not reviews:
                paragraphs = soup.find_all('p')
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if 20 <= len(text) <= 2000:
                        reviews.append(text)
                        if len(reviews) >= max_reviews:
                            break
            
            logger.info(f"Extracted {len(reviews)} reviews")
            return reviews
            
        except ImportError:
            logger.error("requests or beautifulsoup4 not installed")
            return []
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            return []

# ============================================================================
# INITIALIZE SERVICES
# ============================================================================

# Initialize ML analyzer
analyzer = SimpleSentimentAnalyzer()

# Initialize scraper
scraper = SimpleReviewScraper()

# ============================================================================
# AUTHENTICATION HELPERS
# ============================================================================

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current logged in user"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_text_hash(text):
    """Generate hash for deduplication"""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def is_duplicate(text):
    """Check if review already exists"""
    text_hash = generate_text_hash(text)
    return Review.query.filter_by(text_hash=text_hash).first() is not None

# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/')
def index():
    """Main dashboard page - redirect to login if not authenticated"""
    if 'user_id' not in session:
        return send_from_directory('static', 'login.html')
    return send_from_directory('static', 'index.html')

@app.route('/login')
def login_page():
    """Login page"""
    return send_from_directory('static', 'login.html')

@app.route('/signup')
def signup_page():
    """Signup page"""
    return send_from_directory('static', 'signup.html')

@app.route('/api/signup', methods=['POST'])
def signup():
    """User signup endpoint"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        # Validation
        if not username or not email or not password:
            return jsonify({'error': 'All fields are required'}), 400
        
        if len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Log user in
        session['user_id'] = user.id
        session['username'] = user.username
        
        logger.info(f"New user registered: {username}")
        
        return jsonify({
            'message': 'Account created successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Signup error: {e}", exc_info=True)
        db.session.rollback()
        return jsonify({'error': 'Signup failed'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Log user in
        session['user_id'] = user.id
        session['username'] = user.username
        
        logger.info(f"User logged in: {username}")
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Login error: {e}", exc_info=True)
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    username = session.get('username', 'Unknown')
    session.clear()
    logger.info(f"User logged out: {username}")
    return jsonify({'message': 'Logout successful'})

@app.route('/api/me')
@login_required
def get_current_user_info():
    """Get current user information"""
    user = get_current_user()
    if user:
        return jsonify(user.to_dict())
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': 'development',
        'database': 'sqlite',
        'total_reviews': Review.query.count()
    })

@app.route('/api/analyze', methods=['POST'])
@login_required
def analyze_text():
    """Analyze sentiment of provided text"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if len(text) < 5:
            return jsonify({'error': 'Text too short (minimum 5 characters)'}), 400
        
        # Check for duplicate
        if is_duplicate(text):
            logger.info("Duplicate text detected, skipping save")
            result = analyzer.analyze(text)
            result['duplicate'] = True
            return jsonify(result)
        
        # Analyze sentiment
        result = analyzer.analyze(text)
        
        # Save to database
        review = Review(
            text=text,
            sentiment=result['sentiment'],
            emotion=result['emotion'],
            confidence=result['confidence'],
            source='manual_input',
            text_hash=generate_text_hash(text)
        )
        db.session.add(review)
        db.session.commit()
        
        logger.info(f"Analyzed text: {result['sentiment']} ({result['confidence']:.2f})")
        
        result['saved'] = True
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Analysis error: {e}", exc_info=True)
        db.session.rollback()
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/scrape', methods=['POST'])
@login_required
def scrape_reviews_endpoint():
    """Scrape reviews from provided URL"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        max_reviews = min(int(data.get('max_reviews', 10)), 50)  # Limit to 50
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Simple URL validation
        if not (url.startswith('http://') or url.startswith('https://')):
            return jsonify({'error': 'Invalid URL format (must start with http:// or https://)'}), 400
        
        logger.info(f"Starting scrape for: {url}")
        
        # Scrape reviews
        reviews_text = scraper.scrape_reviews(url, max_reviews)
        
        if not reviews_text:
            return jsonify({'error': 'No reviews found at this URL'}), 404
        
        # Analyze each review
        results = []
        saved_count = 0
        duplicate_count = 0
        
        for text in reviews_text:
            try:
                # Check for duplicate
                if is_duplicate(text):
                    duplicate_count += 1
                    continue
                
                analysis = analyzer.analyze(text)
                
                # Save to database
                review = Review(
                    text=text,
                    sentiment=analysis['sentiment'],
                    emotion=analysis['emotion'],
                    confidence=analysis['confidence'],
                    source='scraped',
                    url=url,
                    text_hash=generate_text_hash(text)
                )
                db.session.add(review)
                results.append(analysis)
                saved_count += 1
                
            except Exception as e:
                logger.error(f"Failed to analyze review: {e}")
                continue
        
        db.session.commit()
        
        logger.info(f"Scraped {len(reviews_text)} reviews, saved {saved_count}, skipped {duplicate_count} duplicates")
        
        return jsonify({
            'message': 'Scraping completed successfully',
            'total_found': len(reviews_text),
            'saved': saved_count,
            'duplicates': duplicate_count,
            'url': url,
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Scraping error: {e}", exc_info=True)
        db.session.rollback()
        return jsonify({'error': f'Scraping failed: {str(e)}'}), 500

@app.route('/api/reviews')
@login_required
def get_reviews():
    """Get paginated reviews"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        reviews = Review.query.order_by(Review.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'reviews': [review.to_dict() for review in reviews.items],
            'total': reviews.total,
            'pages': reviews.pages,
            'current_page': page,
            'per_page': per_page
        })
        
    except Exception as e:
        logger.error(f"Error fetching reviews: {e}")
        return jsonify({'error': 'Failed to fetch reviews'}), 500

@app.route('/api/dashboard')
@login_required
def get_dashboard_data():
    """Get dashboard analytics data"""
    try:
        # Get all reviews
        reviews = Review.query.all()
        
        if not reviews:
            return jsonify({
                'total_reviews': 0,
                'sentiment_distribution': {'positive': 0, 'negative': 0, 'neutral': 0},
                'emotion_distribution': {},
                'average_confidence': 0,
                'recent_reviews': []
            })
        
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
        
        avg_confidence = sum(r.confidence for r in reviews) / total_reviews
        
        # Get recent reviews
        recent_reviews = Review.query.order_by(Review.created_at.desc()).limit(10).all()
        
        return jsonify({
            'total_reviews': total_reviews,
            'sentiment_distribution': sentiment_counts,
            'emotion_distribution': emotion_counts,
            'average_confidence': round(avg_confidence, 3),
            'recent_reviews': [r.to_dict() for r in recent_reviews]
        })
        
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return jsonify({'error': 'Failed to load dashboard data'}), 500

@app.route('/api/sentiment-trends')
@login_required
def get_sentiment_trends():
    """Get sentiment trends over time for chart"""
    try:
        from collections import defaultdict
        from datetime import timedelta
        
        # Get all reviews ordered by creation time
        reviews = Review.query.order_by(Review.created_at.asc()).all()
        
        if not reviews:
            return jsonify({
                'labels': [],
                'positive': [],
                'negative': [],
                'neutral': []
            })
        
        # Group reviews by time intervals (hourly or daily depending on data range)
        time_groups = defaultdict(lambda: {'positive': 0, 'negative': 0, 'neutral': 0})
        
        # Determine if we should group by hour or day
        time_range = (reviews[-1].created_at - reviews[0].created_at).total_seconds()
        group_by_hour = time_range < 86400 * 2  # Less than 2 days, group by hour
        
        for review in reviews:
            if group_by_hour:
                # Group by hour
                time_key = review.created_at.strftime('%Y-%m-%d %H:00')
            else:
                # Group by day
                time_key = review.created_at.strftime('%Y-%m-%d')
            
            time_groups[time_key][review.sentiment] += 1
        
        # Sort by time and prepare data
        sorted_times = sorted(time_groups.keys())
        
        # Limit to last 50 data points for better visualization
        if len(sorted_times) > 50:
            sorted_times = sorted_times[-50:]
        
        labels = []
        positive_data = []
        negative_data = []
        neutral_data = []
        
        for time_key in sorted_times:
            # Format label
            if group_by_hour:
                # Show hour format
                dt = datetime.strptime(time_key, '%Y-%m-%d %H:00')
                labels.append(dt.strftime('%m/%d %H:%M'))
            else:
                # Show date format
                dt = datetime.strptime(time_key, '%Y-%m-%d')
                labels.append(dt.strftime('%m/%d'))
            
            positive_data.append(time_groups[time_key]['positive'])
            negative_data.append(time_groups[time_key]['negative'])
            neutral_data.append(time_groups[time_key]['neutral'])
        
        return jsonify({
            'labels': labels,
            'positive': positive_data,
            'negative': negative_data,
            'neutral': neutral_data
        })
        
    except Exception as e:
        logger.error(f"Sentiment trends error: {e}", exc_info=True)
        return jsonify({'error': 'Failed to load sentiment trends'}), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# INITIALIZATION
# ============================================================================

def create_tables():
    """Create database tables"""
    with app.app_context():
        db.create_all()
        logger.info("Database tables created")

def add_sample_data():
    """Add sample data for demo"""
    with app.app_context():
        if Review.query.count() == 0:
            sample_reviews = [
                ("This product is absolutely amazing! I love it so much!", "positive", "happy", 0.9),
                ("Terrible experience, would not recommend to anyone.", "negative", "angry", 0.85),
                ("It's okay, nothing special but works fine for basic needs.", "neutral", "neutral", 0.6),
                ("Outstanding quality and excellent customer service!", "positive", "happy", 0.95),
                ("Very disappointed with the poor quality and late delivery.", "negative", "sad", 0.88)
            ]
            
            for text, sentiment, emotion, confidence in sample_reviews:
                review = Review(
                    text=text,
                    sentiment=sentiment,
                    emotion=emotion,
                    confidence=confidence,
                    source='sample_data',
                    text_hash=generate_text_hash(text)
                )
                db.session.add(review)
            
            db.session.commit()
            logger.info("Sample data added")


# MAIN APPLICATION


if __name__ == '__main__':
    # Initialize database
    create_tables()
    add_sample_data()
    
    logger.info("=" * 70)
    logger.info("🎯 SENTIMENT ANALYSIS DASHBOARD - DEVELOPMENT VERSION")
    logger.info("=" * 70)
    logger.info("📍 URL: http://localhost:5000")
    logger.info("🔧 Mode: Development (no Docker, no Celery)")
    logger.info("💾 Database: SQLite (sentiment_dev.db)")
    logger.info("🤖 ML Model: Lightweight keyword-based")
    logger.info("📝 Note: Production features intentionally removed")
    logger.info("=" * 70)
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # Prevent double initialization
    )
