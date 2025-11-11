# Sentiment Analysis Dashboard - Development Version

A simple, stable sentiment analysis dashboard for development and testing.

## 🚀 Quick Start

```powershell
# Install dependencies
pip install -r requirements_file/requirements_dev.txt

# Run the app
python app_dev.py
```

Then open: **http://localhost:5000**

### Even Easier (Windows)
Double-click: `Bat\START_DEV.bat`

Or use PowerShell: `.\Ps1\START_DEV.ps1`

## 📁 Project Structure

```
.
├── app_dev.py              # Main application (run this!)
├── static/                # Frontend files
├── docs/                  # Documentation
├── python/                # Other Python files (archived)
├── Bat/                   # Batch scripts
│   └── START_DEV.bat      # Easy startup (Windows)
├── Ps1/                   # PowerShell scripts
│   └── START_DEV.ps1
└── requirements_file/     # Requirements and guides
    ├── requirements_dev.txt
    ├── SCRAPING_GUIDE.txt
    └── PROJECT_SUMMARY.txt
```

## 📚 Documentation

All documentation is in the **`docs/`** folder:
- **docs/START_HERE.md** - Start here!
- **docs/QUICKSTART.md** - 3-step setup guide
- **docs/README_DEV.md** - Full documentation
- **requirements_file/SCRAPING_GUIDE.txt** - Web scraping guide

## ✨ Features

- Text sentiment analysis (positive/negative/neutral)
- Emotion detection
- Web scraping with robots.txt respect
- SQLite database
- RESTful API
- Web dashboard

## 📝 Note

This is the **development version**. Production features (Docker, Celery, PostgreSQL, etc.) have been intentionally removed for simplicity and stability. They will be added when requested.

See **docs/PRODUCTION_FEATURES.md** for details.

---

## 📚 More Documentation

### Getting Started
- **[docs/HOW_TO_RUN.md](docs/HOW_TO_RUN.md)** - Quick start guide
- **[docs/README_FIRST.md](docs/README_FIRST.md)** - Complete overview
- **[docs/START_PRODUCTION.md](docs/START_PRODUCTION.md)** - Production setup

### Full Documentation
- **[docs/INDEX.md](docs/INDEX.md)** - Documentation index
- **[docs/README_PRODUCTION.md](docs/README_PRODUCTION.md)** - Production features
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture
- **[docs/FEATURES_SUMMARY.md](docs/FEATURES_SUMMARY.md)** - All features

### Guides
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - Quick start
- **[docs/PRODUCTION_SETUP.md](docs/PRODUCTION_SETUP.md)** - Production deployment
- **[docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md)** - Upgrade guide
- **[docs/COMPARISON.md](docs/COMPARISON.md)** - Old vs New comparison

---

## 🎯 Two Versions Available

### 1. Simple Version (app_simple.py)
- ✅ Easy to run
- ✅ No Redis needed
- ✅ Login system included
- ✅ All basic features
- **Perfect for: Development, Testing, Learning**

```bash
python app_simple.py
```

### 2. Production Version (app_production.py)
- ✅ Full enterprise features
- ✅ Redis caching
- ✅ Celery async tasks
- ✅ JWT authentication
- ✅ Docker support
- **Perfect for: Production, Scaling, Enterprise**

```bash
docker-compose up -d
```

---

## 📊 Features

### Simple Version
- 🔐 Login system with session management
- 🤖 AI sentiment analysis (BERT)
- 🌐 Multi-source web scraping
- 📊 Analytics dashboard
- 💾 SQLite database

### Production Version
- Everything in Simple +
- ⚡ Redis caching (10x faster)
- 🔄 Async task processing (Celery)
- 🔐 JWT authentication
- 📈 Advanced monitoring
- 🧪 Comprehensive testing
- 🐳 Docker deployment
- 📊 Enhanced analytics

---

## 🚀 Quick Commands

```bash
# Run simple version
python app_simple.py

# Add users manually
python add_user.py

# Run production version
python app_production.py

# Docker deployment
docker-compose up -d
```

---

## 📁 Project Structure

```
sentiment-analysis/
├── docs/                    # All documentation
├── app_simple.py           # Simple version (start here!)
├── app_production.py       # Production version
├── add_user.py             # User management tool
├── api/                    # API endpoints
├── models/                 # Database models
├── services/               # Business logic
├── templates/              # HTML templates
├── static/                 # CSS, JS files
└── tests/                  # Test suite
```

---

## 🔐 User Management

### Default User
- Username: `admin`
- Password: `admin123`

### Add More Users
```bash
python add_user.py
```

---

## 🆘 Need Help?

1. **Quick Start**: See [docs/HOW_TO_RUN.md](docs/HOW_TO_RUN.md)
2. **Full Guide**: See [docs/README_FIRST.md](docs/README_FIRST.md)
3. **All Docs**: See [docs/INDEX.md](docs/INDEX.md)

---

## 💡 Recommended Path

1. ✅ Start with `app_simple.py`
2. ✅ Read [docs/HOW_TO_RUN.md](docs/HOW_TO_RUN.md)
3. ✅ Test all features
4. ✅ Explore production version when ready

---

**Built with ❤️ for production use**

🚀 **Start now:** `python app_simple.py`
