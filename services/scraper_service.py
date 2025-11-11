"""
Enhanced scraper service with proxy support and retry logic
"""
from services.review_scraper import ReviewScraper
from core.monitoring import monitor_performance
import logging
import time

logger = logging.getLogger(__name__)

class ScraperService:
    def __init__(self, use_proxy=False, proxy_list=None):
        self.scraper = ReviewScraper()
        self.use_proxy = use_proxy
        self.proxy_list = proxy_list or []
        self.current_proxy_index = 0
    
    def get_next_proxy(self):
        """Get next proxy from list"""
        if not self.proxy_list:
            return None
        
        proxy = self.proxy_list[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)
        return proxy
    
    @monitor_performance
    def scrape_with_retry(self, source, url, max_reviews=100, max_retries=3):
        """Scrape with retry logic"""
        last_error = None
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Scraping attempt {attempt + 1}/{max_retries} for {source}")
                
                reviews = self.scraper.scrape(source, url)
                
                if reviews:
                    logger.info(f"Successfully scraped {len(reviews)} reviews from {source}")
                    return reviews[:max_reviews]
                else:
                    logger.warning(f"No reviews found on attempt {attempt + 1}")
                    
            except Exception as e:
                last_error = e
                logger.error(f"Scraping attempt {attempt + 1} failed: {e}")
                
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5  # Exponential backoff
                    logger.info(f"Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
        
        # All retries failed
        error_msg = f"Failed to scrape after {max_retries} attempts: {last_error}"
        logger.error(error_msg)
        raise Exception(error_msg)
