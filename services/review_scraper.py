import requests
from bs4 import BeautifulSoup
import time
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ReviewScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
    def get_driver(self):
        """Initialize Chrome driver with options"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    
    def scrape(self, source, url):
        """Main scraping method - routes to appropriate scraper"""
        print(f"\n{'='*50}")
        print(f"Scraping {source} from: {url}")
        print(f"{'='*50}\n")
        
        if source == 'google_maps':
            return self.scrape_google_maps(url)
        elif source == 'tripadvisor':
            return self.scrape_tripadvisor(url)
        elif source == 'yelp':
            return self.scrape_yelp(url)
        elif source == 'hotel':
            return self.scrape_hotel(url)
        elif source == 'amazon':
            return self.scrape_amazon(url)
        elif source == 'wikipedia':
            return self.scrape_wikipedia(url)
        else:
            return self.scrape_generic(url)
    
    def scrape_amazon(self, url):
        """Scrape Amazon product reviews"""
        reviews = []
        driver = None
        
        try:
            print(f"Starting Amazon scraping for: {url}")
            driver = self.get_driver()
            driver.get(url)
            time.sleep(5)
            
            # Try to navigate to reviews section
            try:
                reviews_link = driver.find_element(By.XPATH, "//a[@data-hook='see-all-reviews-link-foot']")
                reviews_link.click()
                time.sleep(3)
            except:
                print("Could not find reviews link")
            
            # Scroll to load reviews
            for i in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Amazon review selectors
            review_selectors = [
                "//span[@data-hook='review-body']",
                "//div[@data-hook='review-collapsed']",
                "//span[@class='a-size-base review-text review-text-content']",
            ]
            
            for selector in review_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    print(f"Found {len(elements)} elements")
                    
                    for element in elements:
                        try:
                            text = element.text.strip()
                            if text and len(text) > 20 and text not in reviews:
                                reviews.append(text)
                                print(f"Extracted: {text[:50]}...")
                        except:
                            continue
                    
                    if len(reviews) > 0:
                        break
                except:
                    continue
            
            print(f"Total Amazon reviews: {len(reviews)}")
            
        except Exception as e:
            print(f"Error scraping Amazon: {e}")
        finally:
            if driver:
                driver.quit()
        
        return reviews[:100]
    
    def scrape_generic(self, url):
        """Generic scraper for any website"""
        reviews = []
        driver = None
        
        try:
            print(f"Starting generic scraping for: {url}")
            driver = self.get_driver()
            driver.get(url)
            time.sleep(5)
            
            # Scroll to load content
            for i in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Try to find review-like content
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Look for common review patterns
            review_keywords = ['review', 'comment', 'feedback', 'testimonial', 'rating']
            
            for keyword in review_keywords:
                elements = soup.find_all(['div', 'p', 'span'], class_=re.compile(keyword, re.I))
                
                for element in elements:
                    text = element.get_text(strip=True)
                    if text and len(text) > 30 and len(text) < 1000 and text not in reviews:
                        reviews.append(text)
                        print(f"Extracted: {text[:50]}...")
                
                if len(reviews) > 10:
                    break
            
            print(f"Total generic reviews: {len(reviews)}")
            
        except Exception as e:
            print(f"Error in generic scraping: {e}")
        finally:
            if driver:
                driver.quit()
        
        return reviews[:100]
    
    def scrape_google_maps(self, url):
        """Scrape Google Maps reviews - Enhanced version"""
        reviews = []
        driver = None
        
        try:
            print(f"Starting Google Maps scraping for: {url}")
            driver = self.get_driver()
            driver.get(url)
            
            # Wait for page to load
            time.sleep(5)
            
            # Try to find and click "Reviews" tab
            try:
                reviews_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Reviews')]"))
                )
                reviews_button.click()
                time.sleep(3)
            except:
                print("Reviews tab not found, continuing...")
            
            # Scroll to load more reviews
            scrollable_div = driver.find_element(By.XPATH, "//div[@role='main']")
            for i in range(10):  # Scroll 10 times
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                time.sleep(2)
                print(f"Scrolling... {i+1}/10")
            
            # Extract reviews using multiple selectors
            review_selectors = [
                "//div[@data-review-id]//span[@class='wiI7pd']",
                "//div[contains(@class, 'jftiEf')]",
                "//span[@class='wiI7pd']",
                "//div[@class='MyEned']//span",
            ]
            
            for selector in review_selectors:
                try:
                    review_elements = driver.find_elements(By.XPATH, selector)
                    print(f"Found {len(review_elements)} elements with selector: {selector}")
                    
                    for element in review_elements:
                        try:
                            text = element.text.strip()
                            if text and len(text) > 20 and text not in reviews:
                                reviews.append(text)
                                print(f"Extracted review {len(reviews)}: {text[:50]}...")
                        except:
                            continue
                    
                    if len(reviews) > 0:
                        break
                except Exception as e:
                    print(f"Selector failed: {e}")
                    continue
            
            print(f"Total reviews extracted: {len(reviews)}")
            
        except Exception as e:
            print(f"Error scraping Google Maps: {e}")
        finally:
            if driver:
                driver.quit()
        
        return reviews[:100]  # Limit to 100 reviews
    
    def scrape_tripadvisor(self, url):
        """Scrape TripAdvisor reviews"""
        reviews = []
        driver = None
        
        try:
            print(f"Starting TripAdvisor scraping for: {url}")
            driver = self.get_driver()
            driver.get(url)
            time.sleep(5)
            
            # Scroll to load reviews
            for i in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # TripAdvisor review selectors
            review_selectors = [
                "//div[@data-test-target='review-title']",
                "//div[@class='fIrGe _T']//span",
                "//q[@class='QewHA H4 _a']//span",
                "//div[contains(@class, 'review-text')]",
            ]
            
            for selector in review_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    print(f"Found {len(elements)} elements")
                    
                    for element in elements:
                        try:
                            text = element.text.strip()
                            if text and len(text) > 20 and text not in reviews:
                                reviews.append(text)
                                print(f"Extracted: {text[:50]}...")
                        except:
                            continue
                    
                    if len(reviews) > 0:
                        break
                except:
                    continue
            
            print(f"Total TripAdvisor reviews: {len(reviews)}")
            
        except Exception as e:
            print(f"Error scraping TripAdvisor: {e}")
        finally:
            if driver:
                driver.quit()
        
        return reviews[:100]
    
    def scrape_yelp(self, url):
        """Scrape Yelp reviews"""
        reviews = []
        driver = None
        
        try:
            print(f"Starting Yelp scraping for: {url}")
            driver = self.get_driver()
            driver.get(url)
            time.sleep(5)
            
            # Scroll to load reviews
            for i in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Yelp review selectors
            review_selectors = [
                "//p[@class='comment__09f24__D0cxf css-qgunke']",
                "//span[@class='raw__09f24__T4Ezm']",
                "//p[contains(@class, 'comment')]",
            ]
            
            for selector in review_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    print(f"Found {len(elements)} elements")
                    
                    for element in elements:
                        try:
                            text = element.text.strip()
                            if text and len(text) > 20 and text not in reviews:
                                reviews.append(text)
                                print(f"Extracted: {text[:50]}...")
                        except:
                            continue
                    
                    if len(reviews) > 0:
                        break
                except:
                    continue
            
            print(f"Total Yelp reviews: {len(reviews)}")
            
        except Exception as e:
            print(f"Error scraping Yelp: {e}")
        finally:
            if driver:
                driver.quit()
        
        return reviews[:100]
    
    def scrape_hotel(self, url):
        """Scrape hotel reviews from Booking.com, Hotels.com, etc."""
        reviews = []
        driver = None
        
        try:
            print(f"Starting hotel scraping for: {url}")
            driver = self.get_driver()
            driver.get(url)
            time.sleep(5)
            
            # Scroll to load reviews
            for i in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Generic hotel review selectors
            review_selectors = [
                "//div[@class='c-review-block__row']",
                "//div[contains(@class, 'review-text')]",
                "//div[@itemprop='reviewBody']",
                "//p[@class='review_body']",
                "//div[@class='review-content']",
                "//span[@itemprop='reviewBody']",
            ]
            
            for selector in review_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    print(f"Found {len(elements)} elements")
                    
                    for element in elements:
                        try:
                            text = element.text.strip()
                            if text and len(text) > 20 and text not in reviews:
                                reviews.append(text)
                                print(f"Extracted: {text[:50]}...")
                        except:
                            continue
                    
                    if len(reviews) > 0:
                        break
                except:
                    continue
            
            print(f"Total hotel reviews: {len(reviews)}")
            
        except Exception as e:
            print(f"Error scraping hotel: {e}")
        finally:
            if driver:
                driver.quit()
        
        return reviews[:100]
    
    def scrape_wikipedia(self, url):
        """Scrape Wikipedia content for analysis"""
        reviews = []
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract paragraphs
            paragraphs = soup.find_all('p')
            for p in paragraphs[:20]:
                text = p.get_text(strip=True)
                if text and len(text) > 50:
                    reviews.append(text)
        except Exception as e:
            print(f"Error scraping Wikipedia: {e}")
        
        return reviews
