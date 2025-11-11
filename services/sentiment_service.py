"""
Sentiment analysis service with caching and error handling
"""
from models.sentiment_model import SentimentAnalyzer
from core.extensions import cache
from core.monitoring import monitor_performance
import logging

logger = logging.getLogger(__name__)

class SentimentService:
    def __init__(self):
        self.analyzer = SentimentAnalyzer()
    
    @monitor_performance
    def analyze(self, text):
        """Analyze sentiment with caching"""
        try:
            result = self.analyzer.analyze(text)
            return result
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            raise
    
    @monitor_performance
    def batch_analyze(self, texts, use_cache=True):
        """Batch analyze multiple texts"""
        results = []
        
        for text in texts:
            try:
                if use_cache:
                    cache_key = f"sentiment:{hash(text)}"
                    cached = cache.get(cache_key)
                    if cached:
                        results.append(cached)
                        continue
                
                result = self.analyze(text)
                
                if use_cache:
                    cache.set(cache_key, result, timeout=3600)
                
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to analyze text: {e}")
                results.append({
                    'error': str(e),
                    'sentiment': 'neutral',
                    'emotion': 'neutral',
                    'confidence': 0.0
                })
        
        return results
