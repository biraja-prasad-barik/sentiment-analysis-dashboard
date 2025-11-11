#!/usr/bin/env python3
"""
Test scraping from different URLs
Run with: python test_scraping.py
"""

import requests
import json

# Test URLs
test_urls = [
    "https://www.bbc.com/news",
    "https://example.com",
    "https://www.wikipedia.org/wiki/Sentiment_analysis",
]

print("=" * 70)
print("TESTING WEB SCRAPING")
print("=" * 70)
print()

for url in test_urls:
    print(f"Testing: {url}")
    print("-" * 70)
    
    try:
        response = requests.post(
            'http://localhost:5000/api/scrape',
            json={'url': url, 'max_reviews': 5},
            timeout=30
        )
        
        data = response.json()
        
        if response.status_code == 200:
            print(f"✅ SUCCESS")
            print(f"   Found: {data['total_found']} reviews")
            print(f"   Saved: {data['saved']} new reviews")
            print(f"   Duplicates: {data['duplicates']}")
            
            if data['results']:
                print(f"\n   Sample result:")
                result = data['results'][0]
                print(f"   - Sentiment: {result['sentiment']}")
                print(f"   - Emotion: {result['emotion']}")
                print(f"   - Confidence: {result['confidence']:.2f}")
        else:
            print(f"❌ FAILED: {data.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()

print("=" * 70)
print("TESTING COMPLETE")
print("=" * 70)
print()
print("To view all scraped reviews:")
print("1. Open http://localhost:5000")
print("2. Check the 'Recent Reviews' section")
print("3. Or use: GET http://localhost:5000/api/reviews")
