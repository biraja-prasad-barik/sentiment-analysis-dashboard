# 🚀 Production Setup Guide

## Overview

This is a production-ready sentiment analysis platform with enterprise features:

- ✅ Authentication & Authorization (JWT)
- ✅ Async task processing (Celery)
- ✅ Caching (Redis)
- ✅ Rate limiting
- ✅ Monitoring & logging
- ✅ Docker containerization
- ✅ Database migrations
- ✅ API versioning
- ✅ Comprehensive testing
- ✅ Security best practices

---

## 📁 Project Structure

```
sentiment-analysis/
├── api/                    # API endpoints (v1)
│   ├── auth.py            # Authentication
│   ├── routes.py          # Main routes
│   ├── analytics.py       # Analytics endpoints
│   ├── scraping.py        # Scraping endpoints
│   └── health.py          # Health checks
├── config/                 # Configuration
│   └── settings.py        # Environment configs
├── core/                   # Core components
│   ├── extensions.py      # Flask extensions
│   ├── celery_app.py      # Celery setup
│   ├── logging_config.py  # Logging
│   └── monitoring.py      # Metrics
├── models/                 # Database models
│   ├── user.py
│   ├── review.py
│   └── scrape_job.py
├── services/               # Business logic
│   ├── sentiment_service.py
│   └── scraper_service.py
├── tasks/                  # Celery tasks
│   └── scraping_tasks.py
├── utils/                  # Utilities
│   ├── validators.py
│   ├── decorators.py
│   └── helpers.py
├── tests/                  # Test suite
├── templates/              # Frontend
├── static/                 # Static files
├── logs/                   # Application logs
├── migrations/             # Database migrations
├── app_production.py       # Main application
├── docker-compose.yml      # Docker setup
├── Dockerfile
├── nginx.conf              # Nginx config
└── requirements_production.txt
```

---

## 🛠️ Installation

### Option 1: Docker (Recommended)

1. **Clone and setup**
```bash
cd "Sentiment Analyzer Project"
cp .env.example .env
# Edit .env with your settings
```

2. **Build and run**
```bash
docker-compose up -d
```

3. **Check status**
```bash
docker-compose ps
docker-compose logs -f web
```

4. **Access application**
- API: http://localhost:5000
- Health: http://localhost:5000/api/v1/health

### Option 2: Manual Setup

1. **Install dependencies**
```bash
# Install PostgreSQL and Redis
# Windows: Use installers from official websites
# Linux: sudo apt install postgresql redis-server

# Install Python packages
pip install -r requirements_production.txt
```

2. **Setup database**
```bash
# Create PostgreSQL database
createdb sentiment_prod

# Run migrations
flask db upgrade
```

3. **Start Redis**
```bash
redis-server
```

4. **Start Celery worker**
```bash
celery -A core.celery_app worker --loglevel=info
```

5. **Start Celery beat (scheduler)**
```bash
celery -A core.celery_app beat --loglevel=info
```

6. **Start Flask app**
```bash
python app_production.py
```

---

## 🔐 Environment Variables

Create `.env` file from `.env.example`:

```bash
# Required
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=postgresql://user:pass@localhost:5432/sentiment_prod

# Optional
REDIS_URL=redis://localhost:6379/0
SENTRY_DSN=your-sentry-dsn
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

---

## 📊 API Documentation

### Authentication

**Register**
```bash
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "SecurePass123"
}
```

**Login**
```bash
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

### Analysis

**Analyze Text**
```bash
POST /api/v1/analyze
Authorization: Bearer <token>
{
  "text": "This product is amazing!"
}
```

### Scraping

**Start Scraping (Async)**
```bash
POST /api/v1/scrape
Authorization: Bearer <token>
{
  "source": "google_maps",
  "url": "https://maps.google.com/...",
  "max_reviews": 100
}
```

**Check Status**
```bash
GET /api/v1/scrape/status/<task_id>
```

### Analytics

**Dashboard**
```bash
GET /api/v1/analytics/dashboard?days=30
```

**Export Data**
```bash
GET /api/v1/analytics/export?days=30&format=csv
Authorization: Bearer <token>
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# Specific test file
pytest tests/test_api.py

# Verbose output
pytest -v
```

---

## 📈 Monitoring

### Health Checks

```bash
# Basic health
curl http://localhost:5000/api/v1/health

# Detailed health (includes DB, Redis, Celery)
curl http://localhost:5000/api/v1/health/detailed

# Metrics
curl http://localhost:5000/api/v1/metrics
```

### Logs

```bash
# View logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f web
docker-compose logs -f celery_worker
```

---

## 🚀 Deployment

### Deploy to AWS/GCP/Azure

1. **Build Docker image**
```bash
docker build -t sentiment-analysis:latest .
```

2. **Push to registry**
```bash
docker tag sentiment-analysis:latest your-registry/sentiment-analysis:latest
docker push your-registry/sentiment-analysis:latest
```

3. **Deploy with Kubernetes**
```bash
kubectl apply -f k8s/
```

### Deploy to Heroku

```bash
heroku create sentiment-analysis-app
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev
git push heroku main
```

---

## 🔒 Security Checklist

- [x] JWT authentication
- [x] Password hashing (Werkzeug)
- [x] Rate limiting
- [x] Input validation
- [x] SQL injection prevention (SQLAlchemy ORM)
- [x] XSS protection
- [x] CORS configuration
- [x] Security headers (Nginx)
- [x] HTTPS ready
- [x] Environment-based secrets

---

## 📊 Performance Optimization

1. **Caching**: Redis caching for frequent queries
2. **Database**: Indexes on frequently queried fields
3. **Async**: Celery for long-running tasks
4. **Connection pooling**: SQLAlchemy pool
5. **Load balancing**: Nginx reverse proxy
6. **CDN**: Static files served via CDN

---

## 🐛 Troubleshooting

### Database connection error
```bash
# Check PostgreSQL is running
pg_isready

# Check connection string
echo $DATABASE_URL
```

### Redis connection error
```bash
# Check Redis is running
redis-cli ping

# Should return: PONG
```

### Celery not processing tasks
```bash
# Check worker is running
celery -A core.celery_app inspect active

# Restart worker
docker-compose restart celery_worker
```

---

## 📞 Support

For issues or questions:
1. Check logs: `logs/app.log`
2. Check health: `/api/v1/health/detailed`
3. Review documentation
4. Check Docker logs: `docker-compose logs`

---

## 🎯 Next Steps

1. Setup monitoring (Sentry, Prometheus)
2. Configure CI/CD pipeline
3. Setup automated backups
4. Configure SSL certificates
5. Setup domain and DNS
6. Configure email notifications
7. Add more ML models
8. Implement A/B testing

---

**Built with ❤️ for production use**
