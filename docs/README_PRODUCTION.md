# 🚀 Sentiment Analysis Platform - Production Edition

**Enterprise-grade AI-powered sentiment analysis system with async processing, authentication, caching, and comprehensive monitoring.**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Redis](https://img.shields.io/badge/Redis-7-red.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

---

## ✨ Production Features

### 🔐 Security & Authentication
- JWT-based authentication
- Role-based access control (User/Admin)
- Password hashing with Werkzeug
- Rate limiting (Flask-Limiter)
- Input validation & sanitization
- CORS configuration
- Security headers

### ⚡ Performance & Scalability
- Redis caching for fast responses
- Async task processing with Celery
- Database connection pooling
- Optimized database queries with indexes
- Nginx reverse proxy & load balancing
- Docker containerization
- Horizontal scaling ready

### 📊 Monitoring & Logging
- Structured JSON logging
- Health check endpoints
- Application metrics
- Error tracking (Sentry ready)
- Request/response monitoring
- Performance tracking

### 🤖 AI/ML Features
- BERT-based emotion detection
- DistilBERT sentiment analysis
- Batch processing support
- Model caching
- Confidence scores
- Multi-emotion detection

### 🌐 Web Scraping
- Async scraping with Celery
- Multi-source support (Google Maps, Yelp, TripAdvisor, Amazon)
- Retry logic with exponential backoff
- Proxy support
- Rate limiting per domain
- Progress tracking

### 📈 Analytics & Reporting
- Real-time dashboard
- Sentiment trends over time
- Source comparison
- CSV export
- Custom date ranges
- Emotion distribution

### 🧪 Testing & Quality
- Comprehensive test suite (pytest)
- Unit tests
- Integration tests
- Code coverage reports
- CI/CD ready

---

## 🏗️ Architecture

```
┌─────────────┐
│   Nginx     │  ← Reverse Proxy, Load Balancer
└──────┬──────┘
       │
┌──────▼──────┐
│   Flask     │  ← Web Application (Gunicorn)
│   API v1    │
└──────┬──────┘
       │
┌──────▼──────┬──────────┬──────────┐
│ PostgreSQL  │  Redis   │  Celery  │
│  Database   │  Cache   │  Workers │
└─────────────┴──────────┴──────────┘
```

---

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# 1. Clone repository
cd "Sentiment Analyzer Project"

# 2. Setup environment
cp .env.example .env
# Edit .env with your settings

# 3. Start all services
docker-compose up -d

# 4. Initialize database
docker-compose exec web python scripts/init_db.py

# 5. Access application
# API: http://localhost:5000
# Health: http://localhost:5000/api/v1/health
```

### Manual Setup

```bash
# 1. Install dependencies
pip install -r requirements_production.txt

# 2. Install Redis & PostgreSQL
# Windows: Download installers
# Linux: sudo apt install redis-server postgresql

# 3. Setup database
createdb sentiment_prod
python scripts/init_db.py

# 4. Start services
# Terminal 1: Redis
redis-server

# Terminal 2: Celery Worker
celery -A core.celery_app worker --loglevel=info

# Terminal 3: Celery Beat
celery -A core.celery_app beat --loglevel=info

# Terminal 4: Flask
python app_production.py
```

---

## 📚 API Documentation

### Authentication

**Register User**
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "SecurePass123"
}
```

**Login**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### Analysis

**Analyze Text**
```http
POST /api/v1/analyze
Authorization: Bearer <token>
Content-Type: application/json

{
  "text": "This product is absolutely amazing! Best purchase ever!"
}

Response:
{
  "sentiment": "positive",
  "emotion": "happy",
  "confidence": 0.9876,
  "all_emotions": {
    "joy": 0.9876,
    "sadness": 0.0012,
    "anger": 0.0008
  }
}
```

### Scraping (Async)

**Start Scraping**
```http
POST /api/v1/scrape
Authorization: Bearer <token>
Content-Type: application/json

{
  "source": "google_maps",
  "url": "https://www.google.com/maps/place/...",
  "max_reviews": 100
}

Response:
{
  "message": "Scraping task started",
  "task_id": "abc-123-def-456",
  "status": "pending",
  "estimated_time": "30-120 seconds"
}
```

**Check Status**
```http
GET /api/v1/scrape/status/abc-123-def-456

Response (Processing):
{
  "task_id": "abc-123-def-456",
  "status": "processing",
  "message": "Scraping in progress..."
}

Response (Completed):
{
  "task_id": "abc-123-def-456",
  "status": "completed",
  "result": {
    "job_id": 42,
    "reviews_scraped": 87,
    "reviews_saved": 87,
    "source": "google_maps"
  }
}
```

### Analytics

**Dashboard**
```http
GET /api/v1/analytics/dashboard?days=30

Response:
{
  "total_reviews": 1250,
  "sentiment_distribution": {
    "positive": 750,
    "negative": 300,
    "neutral": 200
  },
  "emotion_distribution": {
    "happy": 600,
    "sad": 200,
    "angry": 150,
    "satisfied": 300
  },
  "satisfaction_score": 60.0,
  "trend_data": [...]
}
```

**Export Data**
```http
GET /api/v1/analytics/export?days=30&format=csv
Authorization: Bearer <token>

Response: CSV file download
```

### Health & Monitoring

**Health Check**
```http
GET /api/v1/health

Response:
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "service": "sentiment-analysis-api"
}
```

**Detailed Health**
```http
GET /api/v1/health/detailed

Response:
{
  "status": "healthy",
  "checks": {
    "database": {"status": "healthy"},
    "cache": {"status": "healthy"},
    "celery": {"status": "healthy", "workers": 2}
  }
}
```

**Metrics**
```http
GET /api/v1/metrics

Response:
{
  "requests_total": 15420,
  "errors_total": 23,
  "avg_response_time_ms": 145.67,
  "database": {
    "total_reviews": 5000,
    "total_users": 150
  }
}
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# Specific test
pytest tests/test_api.py::test_health_check

# Verbose
pytest -v

# View coverage report
open htmlcov/index.html
```

---

## 📊 Monitoring

### Logs

```bash
# Application logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f web
docker-compose logs -f celery_worker

# Filter errors
grep ERROR logs/app.log
```

### Metrics

```bash
# Application metrics
curl http://localhost:5000/api/v1/metrics

# Health status
curl http://localhost:5000/api/v1/health/detailed

# Celery tasks
celery -A core.celery_app inspect active
celery -A core.celery_app inspect stats
```

---

## 🚀 Deployment

### Docker Compose (Production)

```bash
# Build and start
docker-compose up -d

# Scale workers
docker-compose up -d --scale celery_worker=4

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Kubernetes

```bash
# Apply configurations
kubectl apply -f k8s/

# Check status
kubectl get pods
kubectl get services

# Scale
kubectl scale deployment sentiment-web --replicas=3
```

### Cloud Platforms

**AWS**
- ECS/EKS for containers
- RDS for PostgreSQL
- ElastiCache for Redis
- S3 for static files
- CloudWatch for monitoring

**GCP**
- Cloud Run / GKE
- Cloud SQL
- Memorystore
- Cloud Storage
- Cloud Logging

**Azure**
- Container Instances / AKS
- Azure Database for PostgreSQL
- Azure Cache for Redis
- Blob Storage
- Application Insights

---

## 🔒 Security Best Practices

✅ **Implemented**
- JWT authentication
- Password hashing
- Rate limiting
- Input validation
- SQL injection prevention
- XSS protection
- CORS configuration
- Security headers
- Environment-based secrets

🔜 **Recommended**
- Enable HTTPS (SSL/TLS)
- Setup WAF (Web Application Firewall)
- Implement 2FA
- Regular security audits
- Dependency scanning
- Penetration testing

---

## 📈 Performance Tips

1. **Caching**: Enabled by default with Redis
2. **Database**: Indexes on frequently queried fields
3. **Async**: Use Celery for long-running tasks
4. **CDN**: Serve static files via CDN
5. **Load Balancing**: Use Nginx or cloud load balancer
6. **Monitoring**: Track slow queries and endpoints

---

## 🐛 Troubleshooting

### Common Issues

**Redis Connection Error**
```bash
# Check if Redis is running
redis-cli ping

# Start Redis
redis-server
```

**Database Connection Error**
```bash
# Check PostgreSQL
pg_isready

# Check connection string
echo $DATABASE_URL
```

**Celery Not Processing**
```bash
# Check workers
celery -A core.celery_app inspect active

# Restart worker
docker-compose restart celery_worker
```

**Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements_production.txt
```

---

## 📁 Project Structure

```
sentiment-analysis/
├── api/                    # API endpoints
│   ├── auth.py            # Authentication
│   ├── routes.py          # Main routes
│   ├── analytics.py       # Analytics
│   ├── scraping.py        # Scraping
│   └── health.py          # Health checks
├── config/                 # Configuration
├── core/                   # Core components
├── models/                 # Database models
├── services/               # Business logic
├── tasks/                  # Celery tasks
├── utils/                  # Utilities
├── tests/                  # Test suite
├── templates/              # Frontend
├── static/                 # Static files
├── logs/                   # Logs
├── scripts/                # Helper scripts
├── app_production.py       # Main app
├── docker-compose.yml      # Docker setup
├── Dockerfile
└── requirements_production.txt
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is for educational and portfolio purposes.

---

## 📞 Support

- **Documentation**: See `PRODUCTION_SETUP.md`
- **Migration**: See `MIGRATION_GUIDE.md`
- **Issues**: Check logs and health endpoints
- **Questions**: Review API documentation

---

## 🎯 Roadmap

- [x] Authentication & Authorization
- [x] Async task processing
- [x] Caching layer
- [x] Monitoring & logging
- [x] Docker containerization
- [x] Comprehensive testing
- [ ] GraphQL API
- [ ] WebSocket support
- [ ] Multi-language support
- [ ] Advanced ML models
- [ ] Mobile app
- [ ] Admin dashboard

---

**Built with ❤️ for production use**

**Tech Stack**: Flask • PostgreSQL • Redis • Celery • Docker • BERT • Selenium • Nginx
