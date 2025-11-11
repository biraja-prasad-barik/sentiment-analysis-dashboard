"""
Celery tasks for async scraping
"""
from core.celery_app import celery
from core.extensions import db
from models import Review, ScrapeJob
from services.scraper_service import ScraperService
from services.sentiment_service import SentimentService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@celery.task(bind=True, max_retries=3)
def scrape_reviews_task(self, source, url, max_reviews=100, user_id=None):
    """
    Async task to scrape and analyze reviews
    """
    job = None
    
    try:
        # Create scrape job record
        job = ScrapeJob(
            task_id=self.request.id,
            source=source,
            url=url,
            status='processing',
            user_id=user_id,
            started_at=datetime.utcnow()
        )
        db.session.add(job)
        db.session.commit()
        
        logger.info(f"Starting scrape job {job.id} for {source}")
        
        # Initialize services
        scraper = ScraperService()
        sentiment_service = SentimentService()
        
        # Scrape reviews
        reviews_text = scraper.scrape_with_retry(source, url, max_reviews)
        
        if not reviews_text:
            raise Exception("No reviews found")
        
        logger.info(f"Scraped {len(reviews_text)} reviews, starting analysis...")
        
        # Analyze reviews
        results = sentiment_service.batch_analyze(reviews_text)
        
        # Save to database
        saved_count = 0
        for text, result in zip(reviews_text, results):
            if 'error' not in result:
                review = Review(
                    text=text,
                    sentiment=result['sentiment'],
                    emotion=result['emotion'],
                    confidence=result['confidence'],
                    source=source,
                    user_id=user_id,
                    scrape_job_id=job.id
                )
                db.session.add(review)
                saved_count += 1
        
        # Update job status
        job.status = 'completed'
        job.reviews_count = saved_count
        job.completed_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Scrape job {job.id} completed - {saved_count} reviews saved")
        
        return {
            'job_id': job.id,
            'status': 'completed',
            'reviews_scraped': len(reviews_text),
            'reviews_saved': saved_count,
            'source': source
        }
        
    except Exception as e:
        logger.error(f"Scrape task failed: {e}")
        
        if job:
            job.status = 'failed'
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            db.session.commit()
        
        # Retry logic
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))
        
        return {
            'status': 'failed',
            'error': str(e)
        }


@celery.task
def cleanup_old_reviews(days=90):
    """
    Cleanup old reviews (scheduled task)
    """
    from datetime import timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    deleted = Review.query.filter(Review.created_at < cutoff_date).delete()
    db.session.commit()
    
    logger.info(f"Cleaned up {deleted} old reviews")
    return {'deleted': deleted}


@celery.task
def generate_daily_analytics():
    """
    Generate daily analytics summary (scheduled task)
    """
    from models import Analytics
    from datetime import date
    
    today = date.today()
    
    # Check if already exists
    existing = Analytics.query.filter_by(date=today).first()
    if existing:
        logger.info(f"Analytics for {today} already exists")
        return
    
    # Get today's reviews
    reviews = Review.query.filter(
        db.func.date(Review.created_at) == today
    ).all()
    
    if not reviews:
        logger.info(f"No reviews for {today}")
        return
    
    # Calculate stats
    analytics = Analytics(
        date=today,
        total_reviews=len(reviews),
        positive_count=sum(1 for r in reviews if r.sentiment == 'positive'),
        negative_count=sum(1 for r in reviews if r.sentiment == 'negative'),
        neutral_count=sum(1 for r in reviews if r.sentiment == 'neutral'),
        avg_confidence=sum(r.confidence for r in reviews) / len(reviews)
    )
    
    db.session.add(analytics)
    db.session.commit()
    
    logger.info(f"Generated analytics for {today}")
    return {'date': str(today), 'total_reviews': len(reviews)}
