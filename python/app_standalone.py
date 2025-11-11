"""
Standalone version - No dependencies on production code
Run with: python app_standalone.py
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentiment_standalone.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Initialize database
db = SQLAlchemy(app)

# ============================================================================
# MODELS (Standalone - no imports from other files)
# ============================================================================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20), nullable=False)
    emotion = db.Column(db.String(20), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Analytics(db.Model):
    __tablename__ = 'analytics'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    total_reviews = db.Column(db.Integer, default=0)
    positive_count = db.Column(db.Integer, default=0)
    negative_count = db.Column(db.Integer, default=0)
    neutral_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ============================================================================
# LAZY LOADING FOR ML MODELS (Optional - loads only when needed)
# ============================================================================

_analyzer = None
_scraper = None

def get_analyzer():
    """Lazy load sentiment analyzer"""
    global _analyzer
    if _analyzer is None:
        try:
            from models.sentiment_model import SentimentAnalyzer
            _analyzer = SentimentAnalyzer()
        except Exception as e:
            print(f"⚠️  ML model not available: {e}")
            _analyzer = "unavailable"
    return _analyzer

def get_scraper():
    """Lazy load scraper"""
    global _scraper
    if _scraper is None:
        try:
            from services.review_scraper import ReviewScraper
            _scraper = ReviewScraper()
        except Exception as e:
            print(f"⚠️  Scraper not available: {e}")
            _scraper = "unavailable"
    return _scraper

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    session['user_id'] = user.id
    session['username'] = user.username
    
    return jsonify({
        'message': 'Login successful',
        'username': user.username
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    analyzer = get_analyzer()
    if analyzer == "unavailable":
        return jsonify({'error': 'ML model not available. Install: pip install transformers torch'}), 503
    
    try:
        result = analyzer.analyze(text)
        
        # Save to database
        review = Review(
            text=text,
            sentiment=result['sentiment'],
            emotion=result['emotion'],
            confidence=result['confidence']
        )
        db.session.add(review)
        db.session.commit()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/scrape', methods=['POST'])
def scrape_reviews():
    data = request.json
    source = data.get('source')
    url = data.get('url')
    
    if not source or not url:
        return jsonify({'error': 'Source and URL required'}), 400
    
    scraper = get_scraper()
    if scraper == "unavailable":
        return jsonify({'error': 'Scraper not available. Install: pip install selenium beautifulsoup4'}), 503
    
    analyzer = get_analyzer()
    if analyzer == "unavailable":
        return jsonify({'error': 'ML model not available. Install: pip install transformers torch'}), 503
    
    try:
        reviews = scraper.scrape(source, url)
        
        results = []
        for review_text in reviews:
            try:
                result = analyzer.analyze(review_text)
                review = Review(
                    text=review_text,
                    sentiment=result['sentiment'],
                    emotion=result['emotion'],
                    confidence=result['confidence'],
                    source=source
                )
                db.session.add(review)
                results.append(result)
            except Exception as e:
                continue
        
        db.session.commit()
        
        return jsonify({
            'total_reviews': len(results),
            'results': results
        })
    except Exception as e:
        return jsonify({'error': f'Scraping failed: {str(e)}'}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    reviews = Review.query.all()
    
    total_reviews = len(reviews)
    sentiment_counts = {
        'positive': sum(1 for r in reviews if r.sentiment == 'positive'),
        'negative': sum(1 for r in reviews if r.sentiment == 'negative'),
        'neutral': sum(1 for r in reviews if r.sentiment == 'neutral')
    }
    
    emotion_counts = {}
    for review in reviews:
        emotion_counts[review.emotion] = emotion_counts.get(review.emotion, 0) + 1
    
    trend_data = []
    for i in range(7):
        date = datetime.now() - timedelta(days=6-i)
        day_reviews = Review.query.filter(
            db.func.date(Review.created_at) == date.date()
        ).all()
        
        trend_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'positive': sum(1 for r in day_reviews if r.sentiment == 'positive'),
            'negative': sum(1 for r in day_reviews if r.sentiment == 'negative'),
            'neutral': sum(1 for r in day_reviews if r.sentiment == 'neutral')
        })
    
    return jsonify({
        'total_reviews': total_reviews,
        'sentiment_distribution': sentiment_counts,
        'emotion_distribution': emotion_counts,
        'trend_data': trend_data,
        'satisfaction_score': round((sentiment_counts['positive'] / total_reviews * 100) if total_reviews > 0 else 0, 2)
    })

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    reviews = Review.query.order_by(Review.created_at.desc()).paginate(
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
        'current_page': page
    })

# ============================================================================
# INITIALIZATION
# ============================================================================

def create_default_user():
    """Create default admin user if not exists"""
    with app.app_context():
        db.create_all()
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin user created!")
            print("   Username: admin")
            print("   Password: admin123")
        else:
            print("✅ Admin user already exists")

if __name__ == '__main__':
    create_default_user()
    print("\n🚀 Starting application...")
    print("📍 Open: http://localhost:5000")
    print("🔐 Login with: admin / admin123")
    print("\n⚠️  Note: ML features require: pip install transformers torch")
    print("⚠️  Note: Scraping requires: pip install selenium beautifulsoup4\n")
    
    app.run(debug=True, port=5000)
