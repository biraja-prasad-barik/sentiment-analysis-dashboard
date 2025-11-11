import re
import numpy as np

class SentimentAnalyzer:
    def __init__(self):
        # Lazy loading - models will be loaded only when needed
        self._emotion_classifier = None
        self._sentiment_analyzer = None
        print("✅ Sentiment Analyzer initialized (models will load on first use)")
    
    @property
    def emotion_classifier(self):
        """Lazy load emotion classifier"""
        if self._emotion_classifier is None:
            print("📥 Loading emotion detection model (this may take a moment)...")
            try:
                from transformers import pipeline
                self._emotion_classifier = pipeline(
                    "text-classification",
                    model="j-hartmann/emotion-english-distilroberta-base",
                    return_all_scores=True,
                    device=-1  # Use CPU
                )
                print("✅ Emotion model loaded!")
            except Exception as e:
                print(f"⚠️ Could not load emotion model: {e}")
                print("Using fallback emotion detection...")
                self._emotion_classifier = "fallback"
        return self._emotion_classifier
    
    @property
    def sentiment_analyzer(self):
        """Lazy load sentiment analyzer"""
        if self._sentiment_analyzer is None:
            print("📥 Loading sentiment analysis model...")
            try:
                from transformers import pipeline
                self._sentiment_analyzer = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=-1  # Use CPU
                )
                print("✅ Sentiment model loaded!")
            except Exception as e:
                print(f"⚠️ Could not load sentiment model: {e}")
                print("Using fallback sentiment detection...")
                self._sentiment_analyzer = "fallback"
        return self._sentiment_analyzer
    
    def preprocess_text(self, text):
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove special characters
        text = re.sub(r'[^\w\s]', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.lower()
    
    def fallback_sentiment(self, text):
        """Simple rule-based sentiment analysis as fallback"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 
                         'love', 'best', 'perfect', 'awesome', 'beautiful', 'nice', 'happy']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'poor',
                         'disappointing', 'waste', 'never', 'not', 'no', 'sad', 'angry']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return 'positive', 0.7
        elif neg_count > pos_count:
            return 'negative', 0.7
        else:
            return 'neutral', 0.5
    
    def fallback_emotion(self, text):
        """Simple rule-based emotion detection as fallback"""
        text_lower = text.lower()
        
        emotions = {
            'happy': ['happy', 'joy', 'great', 'excellent', 'love', 'wonderful'],
            'angry': ['angry', 'hate', 'terrible', 'worst', 'awful'],
            'sad': ['sad', 'disappointed', 'unhappy', 'depressed'],
            'satisfied': ['satisfied', 'good', 'nice', 'okay', 'fine'],
            'surprised': ['surprised', 'wow', 'amazing', 'incredible'],
            'anxious': ['worried', 'anxious', 'nervous', 'concerned']
        }
        
        scores = {}
        for emotion, keywords in emotions.items():
            score = sum(1 for word in keywords if word in text_lower)
            scores[emotion] = score / len(keywords)
        
        dominant = max(scores, key=scores.get) if any(scores.values()) else 'neutral'
        return dominant, scores
    
    def analyze(self, text):
        # Preprocess
        clean_text = self.preprocess_text(text)
        
        if not clean_text:
            return {
                'sentiment': 'neutral',
                'emotion': 'neutral',
                'confidence': 0.0,
                'all_emotions': {}
            }
        
        try:
            # Try using ML models
            if self.sentiment_analyzer == "fallback":
                sentiment, confidence = self.fallback_sentiment(clean_text)
            else:
                sentiment_result = self.sentiment_analyzer(clean_text)[0]
                sentiment = 'positive' if sentiment_result['label'] == 'POSITIVE' else 'negative'
                confidence = sentiment_result['score']
            
            if self.emotion_classifier == "fallback":
                dominant_emotion, emotions = self.fallback_emotion(clean_text)
            else:
                emotion_results = self.emotion_classifier(clean_text)[0]
                emotions = {e['label']: e['score'] for e in emotion_results}
                dominant_emotion = max(emotions, key=emotions.get)
                
                # Map emotions to simplified categories
                emotion_map = {
                    'joy': 'happy',
                    'sadness': 'sad',
                    'anger': 'angry',
                    'fear': 'anxious',
                    'love': 'satisfied',
                    'surprise': 'surprised'
                }
                dominant_emotion = emotion_map.get(dominant_emotion, dominant_emotion)
            
            return {
                'sentiment': sentiment,
                'emotion': dominant_emotion,
                'confidence': round(confidence, 4),
                'all_emotions': {k: round(v, 4) for k, v in emotions.items()},
                'original_text': text,
                'processed_text': clean_text
            }
            
        except Exception as e:
            print(f"Error in analysis: {e}")
            # Fallback to rule-based
            sentiment, confidence = self.fallback_sentiment(clean_text)
            dominant_emotion, emotions = self.fallback_emotion(clean_text)
            
            return {
                'sentiment': sentiment,
                'emotion': dominant_emotion,
                'confidence': round(confidence, 4),
                'all_emotions': {k: round(v, 4) for k, v in emotions.items()},
                'original_text': text,
                'processed_text': clean_text
            }
    
    def batch_analyze(self, texts):
        return [self.analyze(text) for text in texts]
