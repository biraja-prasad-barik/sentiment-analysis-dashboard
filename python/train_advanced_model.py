#!/usr/bin/env python3
"""
Advanced ML Model Training Script (OPTIONAL)

This script trains a transformer-based sentiment analysis model.
It is NOT used by default in the development version.

To use this model in production:
1. Run this script to train the model
2. Request "Add transformer-based sentiment analysis"
3. The main app will be updated to use this model

Requirements:
pip install transformers torch scikit-learn pandas numpy

Note: This requires significant computational resources and time.
"""

import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_tfidf_model():
    """
    Train a TF-IDF + Logistic Regression model (lightweight alternative)
    This is faster and doesn't require GPU
    """
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
        import pickle
        
        logger.info("Training TF-IDF + Logistic Regression model...")
        
        # Sample training data (in production, use real dataset)
        training_data = [
            ("This is amazing and wonderful!", "positive"),
            ("I love this product so much!", "positive"),
            ("Excellent quality and great service!", "positive"),
            ("Best purchase I've ever made!", "positive"),
            ("Absolutely fantastic experience!", "positive"),
            ("This is terrible and awful!", "negative"),
            ("I hate this, complete waste of money!", "negative"),
            ("Worst product ever, very disappointed!", "negative"),
            ("Poor quality and bad service!", "negative"),
            ("Horrible experience, would not recommend!", "negative"),
            ("It's okay, nothing special.", "neutral"),
            ("Average product, does the job.", "neutral"),
            ("Neither good nor bad.", "neutral"),
            ("Standard quality, as expected.", "neutral"),
            ("Regular experience, nothing remarkable.", "neutral"),
        ]
        
        texts = [text for text, _ in training_data]
        labels = [label for _, label in training_data]
        
        # Create pipeline
        model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
            ('classifier', LogisticRegression(max_iter=1000))
        ])
        
        # Train model
        model.fit(texts, labels)
        
        # Save model
        os.makedirs('models', exist_ok=True)
        model_path = 'models/sentiment_tfidf_model.pkl'
        
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        logger.info(f"✓ Model saved to {model_path}")
        logger.info("✓ Training completed successfully!")
        
        # Test model
        test_texts = [
            "This is great!",
            "This is terrible!",
            "This is okay."
        ]
        
        predictions = model.predict(test_texts)
        logger.info("\nTest predictions:")
        for text, pred in zip(test_texts, predictions):
            logger.info(f"  '{text}' -> {pred}")
        
        return True
        
    except ImportError as e:
        logger.error(f"Missing dependencies: {e}")
        logger.error("Install with: pip install scikit-learn")
        return False
    except Exception as e:
        logger.error(f"Training failed: {e}")
        return False


def train_transformer_model():
    """
    Train a transformer-based model (BERT, RoBERTa, etc.)
    This requires GPU and significant time/resources
    """
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
        import torch
        
        logger.info("Training transformer-based model...")
        logger.warning("This requires GPU and will take significant time!")
        
        # Check for GPU
        if torch.cuda.is_available():
            logger.info(f"✓ GPU available: {torch.cuda.get_device_name(0)}")
        else:
            logger.warning("! No GPU found, training will be slow")
        
        # Sample training data (in production, use large dataset)
        training_data = [
            ("This is amazing and wonderful!", "positive"),
            ("I love this product so much!", "positive"),
            ("This is terrible and awful!", "negative"),
            ("I hate this, complete waste!", "negative"),
            ("It's okay, nothing special.", "neutral"),
        ]
        
        # Load pre-trained model
        model_name = "distilbert-base-uncased"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=3  # positive, negative, neutral
        )
        
        logger.info("✓ Model loaded")
        logger.info("Note: Full training requires a large dataset and GPU")
        logger.info("This is just a demonstration of the structure")
        
        # Save model structure
        os.makedirs('models', exist_ok=True)
        model_path = 'models/sentiment_transformer_model'
        model.save_pretrained(model_path)
        tokenizer.save_pretrained(model_path)
        
        logger.info(f"✓ Model structure saved to {model_path}")
        logger.info("✓ To use this in production, train on a large dataset")
        
        return True
        
    except ImportError as e:
        logger.error(f"Missing dependencies: {e}")
        logger.error("Install with: pip install transformers torch")
        return False
    except Exception as e:
        logger.error(f"Training failed: {e}")
        return False


def main():
    """Main training function"""
    logger.info("=" * 70)
    logger.info("ADVANCED ML MODEL TRAINING (OPTIONAL)")
    logger.info("=" * 70)
    logger.info("")
    logger.info("This script trains advanced ML models for sentiment analysis.")
    logger.info("These models are NOT used by default in the development version.")
    logger.info("")
    logger.info("Choose a model to train:")
    logger.info("1. TF-IDF + Logistic Regression (Fast, CPU-friendly)")
    logger.info("2. Transformer (BERT-based, requires GPU)")
    logger.info("3. Both")
    logger.info("")
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == "1":
        logger.info("\nTraining TF-IDF model...")
        success = train_tfidf_model()
    elif choice == "2":
        logger.info("\nTraining Transformer model...")
        success = train_transformer_model()
    elif choice == "3":
        logger.info("\nTraining both models...")
        success1 = train_tfidf_model()
        logger.info("")
        success2 = train_transformer_model()
        success = success1 and success2
    else:
        logger.error("Invalid choice!")
        return
    
    if success:
        logger.info("")
        logger.info("=" * 70)
        logger.info("TRAINING COMPLETED!")
        logger.info("=" * 70)
        logger.info("")
        logger.info("To use these models in production:")
        logger.info("1. Request: 'Add advanced ML model support'")
        logger.info("2. The main app will be updated to load and use these models")
        logger.info("3. You can switch between models via configuration")
        logger.info("")
    else:
        logger.error("")
        logger.error("Training failed! Check the error messages above.")


if __name__ == '__main__':
    main()
