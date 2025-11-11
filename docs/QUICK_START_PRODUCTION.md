# ⚡ Quick Start - Production Version

## 🎯 Choose Your Path

### Path 1: Docker (Easiest) 🐳

```bash
# 1. Setup environment
cp .env.example .env

# 2. Start everything
docker-compose up -d

# 3. Initialize database
docker-compose exec web python scripts/init_db.py

# 4. Done! Access at http://localhost:5000
```

**Login credentials:**
- Admin: `admin@sentiment.ai` / `Admin123!`
- Demo: `demo@sentiment.ai` / `Demo123!`

---

### Path 2: Windows Manual Setup 💻

```bash
# 1. Install Redis
# Download from: https://github.com/microsoftarchive/redis/releases
# Extract and run: redis-server.exe

# 2. Install dependencies
pip install -r requirements_production.txt

# 3. Setup environment
copy .env.example .env
notepad .env

# 4. Initialize database
python scripts\init_db.py

# 5. Start services (run each in separate terminal)
# Terminal 1:
redis-server

# Terminal 2:
celery -A core.celery_app worker --loglevel=info --pool=solo

# Terminal 3:
celery -A core.celery_app beat --loglevel=info

# Terminal 4:
python app_production.py

# 6. Access at http://localhost:5000
```

---

### Path 3: Use Start Script 🚀

**Windows:**
```bash
scripts\start_dev.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/start_dev.sh
./scripts/start_dev.sh
```

---

## 🧪 Test It Works

### 1. Health Check
```bash
curl http://localhost:5000/api/v1/health
```

### 2. Register User
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"name\":\"Test User\",\"password\":\"Test123!\"}"
```

### 3. Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"Test123!\"}"
```

### 4. Analyze Text
```bash
curl -X POST http://localhost:5000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"This is amazing! I love it!\"}"
```

---

## 📊 Access Points

- **Main App**: http://localhost:5000
- **API Health**: http://localhost:5000/api/v1/health
- **API Metrics**: http://localhost:5000/api/v1/metrics
- **Analytics**: http://localhost:5000/api/v1/analytics/dashboard

---

## 🔧 Common Issues

### Redis not running
```bash
# Windows: Start redis-server.exe
# Linux: sudo service redis-server start
# Check: redis-cli ping (should return PONG)
```

### Port 5000 in use
```bash
# Change port in .env
PORT=8000
```

### Import errors
```bash
pip install -r requirements_production.txt
```

---

## 📚 Next Steps

1. ✅ Read `README_PRODUCTION.md` for full documentation
2. ✅ Check `PRODUCTION_SETUP.md` for deployment
3. ✅ Review `MIGRATION_GUIDE.md` if upgrading
4. ✅ See `FEATURES_SUMMARY.md` for all features

---

**Need help? Check the logs:**
```bash
# Application logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f web
```

---

**You're ready to go! 🎉**
