# 🚀 START HERE - Production Version

## ⚡ 3-Minute Quick Start

### Step 1: Choose Your Method

#### Option A: Docker (Easiest) 🐳
```bash
# 1. Copy environment file
copy .env.example .env

# 2. Start everything
docker-compose up -d

# 3. Initialize database
docker-compose exec web python scripts/init_db.py

# 4. Done! Open http://localhost:5000
```

#### Option B: Windows Manual 💻
```bash
# 1. Install Redis (download from GitHub releases)
# 2. Install dependencies
pip install -r requirements_production.txt

# 3. Setup environment
copy .env.example .env

# 4. Initialize database
python scripts\init_db.py

# 5. Start services (use scripts)
scripts\start_dev.bat
```

---

## ✅ Verify It Works

### Test 1: Health Check
```bash
curl http://localhost:5000/api/v1/health
```
**Expected:** `{"status": "healthy"}`

### Test 2: Register User
```bash
curl -X POST http://localhost:5000/api/v1/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"name\":\"Test User\",\"password\":\"Test123!\"}"
```
**Expected:** Access token returned

### Test 3: Analyze Text
```bash
curl -X POST http://localhost:5000/api/v1/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"This is amazing! I love it!\"}"
```
**Expected:** Sentiment analysis result

---

## 🎯 What's Different?

### Old Version
```
app.py → Run → Done
```

### Production Version
```
Docker Compose → Multiple Services → Production Ready
  ├── Flask API (Web)
  ├── PostgreSQL (Database)
  ├── Redis (Cache)
  ├── Celery Worker (Async Tasks)
  └── Nginx (Load Balancer)
```

---

## 📚 Next Steps

1. **Read Documentation**
   - `INDEX.md` - Navigation guide
   - `QUICK_START_PRODUCTION.md` - Detailed start
   - `README_PRODUCTION.md` - Full documentation

2. **Explore Features**
   - Authentication (JWT)
   - Async scraping (Celery)
   - Analytics dashboard
   - Health monitoring

3. **Test APIs**
   - Use Postman or curl
   - Try all endpoints
   - Check analytics

4. **Deploy**
   - See `PRODUCTION_SETUP.md`
   - Docker deployment
   - Cloud deployment

---

## 🆘 Quick Troubleshooting

### Redis not running?
```bash
# Windows: Start redis-server.exe
# Linux: sudo service redis-server start
# Check: redis-cli ping
```

### Port 5000 in use?
```bash
# Change in .env
PORT=8000
```

### Import errors?
```bash
pip install -r requirements_production.txt
```

### Docker issues?
```bash
docker-compose down
docker-compose up -d --build
```

---

## 🎓 Default Credentials

After running `scripts/init_db.py`:

**Admin User:**
- Email: `admin@sentiment.ai`
- Password: `Admin123!`

**Demo User:**
- Email: `demo@sentiment.ai`
- Password: `Demo123!`

---

## 📊 Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/auth/register` | POST | Register user |
| `/api/v1/auth/login` | POST | Login |
| `/api/v1/analyze` | POST | Analyze text |
| `/api/v1/scrape` | POST | Start scraping |
| `/api/v1/analytics/dashboard` | GET | Analytics |
| `/api/v1/metrics` | GET | App metrics |

---

## 🎯 Success Checklist

- [ ] Services running (Docker or manual)
- [ ] Health check passes
- [ ] Can register user
- [ ] Can login
- [ ] Can analyze text
- [ ] Can view analytics
- [ ] Logs are working

---

## 💡 Pro Tips

1. **Use Docker** - Easiest way to get started
2. **Check logs** - `logs/app.log` or `docker-compose logs -f`
3. **Test APIs** - Use Postman or curl
4. **Read docs** - Start with `INDEX.md`
5. **Explore code** - Well-organized in folders

---

## 🚀 You're Ready!

The application is now running with:
- ✅ Authentication
- ✅ Caching
- ✅ Async tasks
- ✅ Monitoring
- ✅ Security
- ✅ Scalability

**Access it at: http://localhost:5000**

---

**Need more help? See `INDEX.md` for complete documentation!**
