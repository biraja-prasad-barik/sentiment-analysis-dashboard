# 🔄 Migration Guide: Old → Production

## Overview

This guide helps you migrate from the old simple app to the new production-ready system.

---

## 📊 What Changed?

### Old Structure
```
app.py                    # Everything in one file
models/database.py        # Simple models
services/review_scraper.py
templates/
static/
```

### New Structure
```
app_production.py         # Application factory
api/                      # Organized API endpoints
  ├── auth.py            # Authentication
  ├── routes.py          # Main routes
  ├── analytics.py       # Analytics
  ├── scraping.py        # Async scraping
  └── health.py          # Health checks
config/                   # Environment configs
core/                     # Core components
  ├── extensions.py      # Flask extensions
  ├── celery_app.py      # Async tasks
  ├── logging_config.py  # Structured logging
  └── monitoring.py      # Metrics
models/                   # Enhanced models
  ├── user.py           # User authentication
  ├── review.py         # Reviews
  └── scrape_job.py     # Scraping jobs
services/                 # Business logic
tasks/                    # Celery tasks
utils/                    # Utilities
tests/                    # Test suite
```

---

## 🚀 Migration Steps

### Step 1: Backup Old Data

```bash
# Backup old database
copy sentiment.db sentiment_backup.db

# Or export to CSV
python -c "
from app import app, db, Review
import csv
with app.app_context():
    reviews = Review.query.all()
    with open('reviews_backup.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['text', 'sentiment', 'emotion', 'confidence', 'source'])
        for r in reviews:
            writer.writerow([r.text, r.sentiment, r.emotion, r.confidence, r.source])
"
```

### Step 2: Install New Dependencies

```bash
# Install production requirements
pip install -r requirements_production.txt

# Install Redis (required for caching and Celery)
# Windows: Download from https://github.com/microsoftarchive/redis/releases
# Linux: sudo apt install redis-server
```

### Step 3: Setup Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env with your settings
notepad .env
```

### Step 4: Initialize New Database

```bash
# Initialize database with migrations
python scripts/init_db.py

# This creates:
# - Admin user: admin@sentiment.ai / Admin123!
# - Demo user: demo@sentiment.ai / Demo123!
# - Sample reviews
```

### Step 5: Import Old Data (Optional)

```python
# import_old_data.py
from app_production import create_app
from core.extensions import db
from models import Review
import sqlite3

app = create_app()

with app.app_context():
    # Connect to old database
    old_db = sqlite3.connect('sentiment_backup.db')
    cursor = old_db.cursor()
    
    # Get old reviews
    cursor.execute('SELECT text, sentiment, emotion, confidence, source, created_at FROM reviews')
    
    for row in cursor.fetchall():
        review = Review(
            text=row[0],
            sentiment=row[1],
            emotion=row[2],
            confidence=row[3],
            source=row[4],
            created_at=row[5]
        )
        db.session.add(review)
    
    db.session.commit()
    print(f"Imported {cursor.rowcount} reviews")
```

### Step 6: Start Services

**Option A: Docker (Recommended)**
```bash
docker-compose up -d
```

**Option B: Manual**
```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start Celery Worker
celery -A core.celery_app worker --loglevel=info --pool=solo

# Terminal 3: Start Celery Beat
celery -A core.celery_app beat --loglevel=info

# Terminal 4: Start Flask
python app_production.py
```

**Option C: Use Scripts**
```bash
# Windows
scripts\start_dev.bat

# Linux/Mac
bash scripts/start_dev.sh
```

---

## 🔄 API Changes

### Old API → New API

**Analyze Text**
```bash
# Old
POST /api/analyze
{
  "text": "..."
}

# New (same, but with optional auth)
POST /api/v1/analyze
Authorization: Bearer <token>  # Optional
{
  "text": "..."
}
```

**Scrape Reviews**
```bash
# Old (synchronous, slow)
POST /api/scrape
{
  "source": "google_maps",
  "url": "..."
}
# Response: immediate with results

# New (asynchronous, fast)
POST /api/v1/scrape
Authorization: Bearer <token>  # Optional
{
  "source": "google_maps",
  "url": "...",
  "max_reviews": 100
}
# Response: task_id

# Then check status
GET /api/v1/scrape/status/<task_id>
```

**Analytics**
```bash
# Old
GET /api/analytics

# New (enhanced)
GET /api/v1/analytics/dashboard?days=30
GET /api/v1/analytics/sentiment-trends?days=30
GET /api/v1/analytics/comparison
GET /api/v1/analytics/export?format=csv
```

---

## 🆕 New Features

### 1. Authentication

```bash
# Register
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "SecurePass123"
}

# Login
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "SecurePass123"
}

# Use token in requests
Authorization: Bearer <access_token>
```

### 2. Async Scraping

```bash
# Start scraping (returns immediately)
POST /api/v1/scrape
{
  "source": "google_maps",
  "url": "...",
  "max_reviews": 100
}

# Response
{
  "task_id": "abc-123",
  "status": "pending",
  "estimated_time": "30-120 seconds"
}

# Check status
GET /api/v1/scrape/status/abc-123

# Response when complete
{
  "task_id": "abc-123",
  "status": "completed",
  "result": {
    "reviews_scraped": 50,
    "reviews_saved": 50
  }
}
```

### 3. Enhanced Analytics

```bash
# Dashboard with date range
GET /api/v1/analytics/dashboard?days=30

# Sentiment trends
GET /api/v1/analytics/sentiment-trends?days=30&source=google_maps

# Source comparison
GET /api/v1/analytics/comparison

# Export to CSV
GET /api/v1/analytics/export?days=30&format=csv
```

### 4. Health Monitoring

```bash
# Basic health
GET /api/v1/health

# Detailed (checks DB, Redis, Celery)
GET /api/v1/health/detailed

# Metrics
GET /api/v1/metrics
```

---

## 🎨 Frontend Changes

The old frontend (`templates/index.html`) still works! But you need to update API calls:

### Update JavaScript

```javascript
// Old
fetch('/api/analyze', { ... })

// New
fetch('/api/v1/analyze', { ... })

// Add authentication (optional)
fetch('/api/v1/analyze', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  ...
})

// For scraping, handle async
const response = await fetch('/api/v1/scrape', { ... });
const { task_id } = await response.json();

// Poll for status
const checkStatus = async () => {
  const status = await fetch(`/api/v1/scrape/status/${task_id}`);
  const data = await status.json();
  
  if (data.status === 'completed') {
    // Show results
  } else if (data.status === 'failed') {
    // Show error
  } else {
    // Still processing, check again
    setTimeout(checkStatus, 5000);
  }
};
```

---

## 🔧 Configuration

### Old (hardcoded)
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentiment.db'
app.config['DEBUG'] = True
```

### New (environment-based)
```python
# .env file
FLASK_ENV=development
DATABASE_URL=postgresql://user:pass@localhost/sentiment_prod
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-key
REDIS_URL=redis://localhost:6379/0
```

---

## 📝 Checklist

- [ ] Backup old database
- [ ] Install new dependencies
- [ ] Install Redis
- [ ] Setup .env file
- [ ] Initialize new database
- [ ] Import old data (optional)
- [ ] Start Redis
- [ ] Start Celery worker
- [ ] Start Flask app
- [ ] Test API endpoints
- [ ] Update frontend (if needed)
- [ ] Test scraping
- [ ] Test analytics
- [ ] Check logs

---

## 🐛 Common Issues

### "Redis connection refused"
```bash
# Start Redis
redis-server

# Or on Windows, start from Services
```

### "Celery not processing tasks"
```bash
# Make sure worker is running
celery -A core.celery_app worker --loglevel=info --pool=solo
```

### "Database not found"
```bash
# Initialize database
python scripts/init_db.py
```

### "Import errors"
```bash
# Reinstall dependencies
pip install -r requirements_production.txt
```

---

## 🎯 Next Steps

1. ✅ Complete migration
2. Test all features
3. Deploy to production (Docker)
4. Setup monitoring (Sentry)
5. Configure backups
6. Setup CI/CD
7. Add more features

---

**Need help? Check PRODUCTION_SETUP.md for detailed documentation**
