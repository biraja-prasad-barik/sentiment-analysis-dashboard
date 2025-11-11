from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentiment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import database and models
from models.database import db, Review, Analytics

# Initialize database with app
db.init_app(app)

# Import services
from models.sentiment_model import SentimentAnalyzer
from services.review_scraper import ReviewScraper

# Initialize sentiment analyzer
analyzer = SentimentAnalyzer()
scraper = ReviewScraper()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
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

@app.route('/api/scrape', methods=['POST'])
def scrape_reviews():
    data = request.json
    source = data.get('source')  # 'google_maps', 'hotel', 'wikipedia'
    url = data.get('url')
    
    if not source or not url:
        return jsonify({'error': 'Source and URL required'}), 400
    
    reviews = scraper.scrape(source, url)
    
    # Analyze and save reviews
    results = []
    for review_text in reviews:
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
    
    db.session.commit()
    
    return jsonify({
        'total_reviews': len(results),
        'results': results
    })

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    reviews = Review.query.all()
    
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
    
    # Trend data (last 7 days)
    from datetime import timedelta
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
