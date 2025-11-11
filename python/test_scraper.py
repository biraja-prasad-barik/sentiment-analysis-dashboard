"""
Test script to verify the scraper is working
Run this before starting the main app
"""

from services.review_scraper import ReviewScraper
import sys

def test_scraper():
    print("\n" + "="*60)
    print("TESTING REVIEW SCRAPER")
    print("="*60 + "\n")
    
    scraper = ReviewScraper()
    
    # Test URLs
    test_cases = [
        {
            'name': 'Google Maps - Taj Mahal',
            'source': 'google_maps',
            'url': 'https://www.google.com/maps/place/Taj+Mahal/@27.1751496,78.0399535,17z/data=!3m1!4b1!4m6!3m5!1s0x39747121d702ff6d:0xdd2ae4803f767dde!8m2!3d27.1751448!4d78.0421422!16zL20vMGw1eGI'
        },
        {
            'name': 'TripAdvisor - Sample Hotel',
            'source': 'tripadvisor',
            'url': 'https://www.tripadvisor.com/Hotel_Review-g304551-d306997-Reviews-The_Oberoi_Amarvilas-Agra_Agra_District_Uttar_Pradesh.html'
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {test['name']}")
        print(f"{'='*60}")
        print(f"Source: {test['source']}")
        print(f"URL: {test['url']}")
        print("\nScraping... (this may take 30-60 seconds)\n")
        
        try:
            reviews = scraper.scrape(test['source'], test['url'])
            
            print(f"\n✅ SUCCESS!")
            print(f"Total reviews scraped: {len(reviews)}")
            
            if reviews:
                print("\nSample reviews:")
                for j, review in enumerate(reviews[:3], 1):
                    print(f"\n{j}. {review[:150]}...")
            else:
                print("\n No reviews found. This might be due to:")
                print("   - Website structure changed")
                print("   - Anti-scraping measures")
                print("   - Network issues")
                print("   - Invalid URL")
                
        except Exception as e:
            print(f"\n ERROR: {str(e)}")
            print("\nTroubleshooting:")
            print("1. Make sure Chrome/Chromium is installed")
            print("2. Check your internet connection")
            print("3. Try a different URL")
            
        print("\n" + "="*60)
    
    print("\n\n Testing complete!")
    print("\nIf you see reviews above, the scraper is working!")
    print("You can now run: python app.py")
    print("\n")

if __name__ == "__main__":
    test_scraper()
