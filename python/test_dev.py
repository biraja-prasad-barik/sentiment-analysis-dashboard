#!/usr/bin/env python3
"""
Unit tests for development version
Run with: python -m pytest test_dev.py -v
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app_dev import (
    app, db, Review, SimpleSentimentAnalyzer, 
    generate_text_hash, is_duplicate
)


class TestSentimentAnalyzer(unittest.TestCase):
    """Test sentiment analysis functionality"""
    
    def setUp(self):
        self.analyzer = SimpleSentimentAnalyzer()
    
    def test_positive_sentiment(self):
        """Test positive sentiment detection"""
        text = "This is absolutely amazing and wonderful!"
        result = self.analyzer.analyze(text)
        self.assertEqual(result['sentiment'], 'positive')
        self.assertGreater(result['confidence'], 0.6)
    
    def test_negative_sentiment(self):
        """Test negative sentiment detection"""
        text = "This is terrible and awful, I hate it!"
        result = self.analyzer.analyze(text)
        self.assertEqual(result['sentiment'], 'negative')
        self.assertGreater(result['confidence'], 0.6)
    
    def test_neutral_sentiment(self):
        """Test neutral sentiment detection"""
        text = "This is a regular product with standard features."
        result = self.analyzer.analyze(text)
        self.assertEqual(result['sentiment'], 'neutral')
    
    def test_emotion_detection(self):
        """Test emotion detection"""
        text = "I am so happy and excited about this!"
        result = self.analyzer.analyze(text)
        self.assertEqual(result['emotion'], 'happy')
    
    def test_short_text(self):
        """Test handling of short text"""
        text = "Hi"
        result = self.analyzer.analyze(text)
        self.assertEqual(result['sentiment'], 'neutral')
        self.assertEqual(result['confidence'], 0.5)
    
    def test_empty_text(self):
        """Test handling of empty text"""
        text = ""
        result = self.analyzer.analyze(text)
        self.assertEqual(result['sentiment'], 'neutral')
    
    def test_preprocessing(self):
        """Test text preprocessing"""
        text = "This is GREAT!!! #awesome @user"
        clean = self.analyzer.preprocess_text(text)
        self.assertIn('great', clean)
        self.assertIn('awesome', clean)
        self.assertNotIn('#', clean)
        self.assertNotIn('@', clean)


class TestDatabaseModels(unittest.TestCase):
    """Test database models"""
    
    def setUp(self):
        """Set up test database"""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up test database"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_review_creation(self):
        """Test creating a review"""
        with app.app_context():
            review = Review(
                text="Test review",
                sentiment="positive",
                emotion="happy",
                confidence=0.9,
                source="test",
                text_hash=generate_text_hash("Test review")
            )
            db.session.add(review)
            db.session.commit()
            
            saved_review = Review.query.first()
            self.assertIsNotNone(saved_review)
            self.assertEqual(saved_review.text, "Test review")
            self.assertEqual(saved_review.sentiment, "positive")
    
    def test_review_to_dict(self):
        """Test review serialization"""
        with app.app_context():
            review = Review(
                text="Test review",
                sentiment="positive",
                emotion="happy",
                confidence=0.9,
                source="test",
                text_hash=generate_text_hash("Test review")
            )
            db.session.add(review)
            db.session.commit()
            
            review_dict = review.to_dict()
            self.assertIn('id', review_dict)
            self.assertIn('text', review_dict)
            self.assertIn('sentiment', review_dict)
            self.assertEqual(review_dict['text'], "Test review")
    
    def test_duplicate_detection(self):
        """Test duplicate review detection"""
        with app.app_context():
            text = "Duplicate test review"
            text_hash = generate_text_hash(text)
            
            # Add first review
            review1 = Review(
                text=text,
                sentiment="positive",
                emotion="happy",
                confidence=0.9,
                source="test",
                text_hash=text_hash
            )
            db.session.add(review1)
            db.session.commit()
            
            # Check if duplicate
            self.assertTrue(is_duplicate(text))
            
            # Different text should not be duplicate
            self.assertFalse(is_duplicate("Different text"))


class TestAPIEndpoints(unittest.TestCase):
    """Test API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up test database"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
    
    def test_analyze_endpoint(self):
        """Test text analysis endpoint"""
        response = self.client.post('/api/analyze',
            json={'text': 'This is an amazing product!'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('sentiment', data)
        self.assertIn('emotion', data)
        self.assertIn('confidence', data)
    
    def test_analyze_empty_text(self):
        """Test analysis with empty text"""
        response = self.client.post('/api/analyze',
            json={'text': ''},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_analyze_short_text(self):
        """Test analysis with short text"""
        response = self.client.post('/api/analyze',
            json={'text': 'Hi'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_reviews_endpoint(self):
        """Test reviews listing endpoint"""
        response = self.client.get('/api/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('reviews', data)
        self.assertIn('total', data)
        self.assertIn('pages', data)
    
    def test_dashboard_endpoint(self):
        """Test dashboard data endpoint"""
        response = self.client.get('/api/dashboard')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('total_reviews', data)
        self.assertIn('sentiment_distribution', data)
        self.assertIn('emotion_distribution', data)
    
    def test_scrape_invalid_url(self):
        """Test scraping with invalid URL"""
        response = self.client.post('/api/scrape',
            json={'url': 'not-a-url'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_scrape_missing_url(self):
        """Test scraping without URL"""
        response = self.client.post('/api/scrape',
            json={},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


class TestHelperFunctions(unittest.TestCase):
    """Test helper functions"""
    
    def test_generate_text_hash(self):
        """Test hash generation"""
        text = "Test text"
        hash1 = generate_text_hash(text)
        hash2 = generate_text_hash(text)
        
        # Same text should produce same hash
        self.assertEqual(hash1, hash2)
        
        # Different text should produce different hash
        hash3 = generate_text_hash("Different text")
        self.assertNotEqual(hash1, hash3)
        
        # Hash should be 64 characters (SHA-256)
        self.assertEqual(len(hash1), 64)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
