# 🚀 Complete Setup Guide

This guide ensures anyone can download and run this project successfully.

---

## ✅ Prerequisites

Before starting, make sure you have:

1. **Python 3.8 or higher** installed
   - Check: `python --version`
   - Download: https://www.python.org/downloads/

2. **pip** (Python package manager)
   - Usually comes with Python
   - Check: `pip --version`

3. **Internet connection** (for installing packages and scraping)

---

## 📦 Installation Steps

### For Windows Users (Easiest)

#### Option 1: One-Click Setup (Recommended)

1. **Extract the ZIP file** to any folder
2. **Double-click**: `Bat\START_DEV.bat`
3. **Wait** for dependencies to install (first time only)
4. **Browser opens automatically** at http://localhost:5000
5. **Done!** 🎉

#### Option 2: Manual Setup

1. **Extract the ZIP file**

2. **Open PowerShell or Command Prompt** in the project folder

3. **Install dependencies**:
   ```powershell
   pip install -r requirements_file/requirements_dev.txt
   ```

4. **Run the application**:
   ```powershell
   python app_dev.py
   ```

5. **Open browser**: http://localhost:5000

---

### For Mac/Linux Users

1. **Extract the ZIP file**

2. **Open Terminal** in the project folder

3. **Install dependencies**:
   ```bash
   pip install -r requirements_file/requirements_dev.txt
   ```

4. **Run the application**:
   ```bash
   python app_dev.py
   ```

5. **Open browser**: http://localhost:5000

---

## 🎯 First Time Usage

### Step 1: Create Account

1. Open http://localhost:5000
2. You'll see the **Login page**
3. Click **"Sign up"**
4. Fill in the form:
   - Username (min 3 characters)
   - Email
   - Password (min 6 characters)
   - Confirm password
5. Click **"Create Account"**
6. You'll be automatically logged in!

### Step 2: Test the Dashboard

1. **Analyze Text**:
   - Type: "This product is amazing!"
   - Click "Analyze Sentiment"
   - See result: Positive 😊

2. **Scrape Reviews**:
   - Enter URL: `https://www.bbc.com/news`
   - Max Reviews: `10`
   - Click "Scrape & Analyze"
   - Wait 5-10 seconds
   - See reviews appear!

3. **View Graph**:
   - Scroll down to see the sentiment trend graph
   - Watch it update with your reviews
   - Toggle checkboxes to filter sentiments

---

## 📁 Project Structure

```
sentiment-analysis-dashboard/
│
├── app_dev.py                    # Main application (run this!)
├── README.md                     # Project overview
├── SETUP_GUIDE.md               # This file
│
├── Bat/                         # Windows startup scripts
│   └── START_DEV.bat            # Double-click to start
│
├── Ps1/                         # PowerShell scripts
│   └── START_DEV.ps1
│
├── static/                      # Frontend files
│   ├── index.html               # Main dashboard
│   ├── login.html               # Login page
│   └── signup.html              # Signup page
│
├── requirements_file/           # Dependencies
│   └── requirements_dev.txt     # Python packages
│
├── docs/                        # Documentation
│   ├── START_HERE.md
│   ├── QUICKSTART.md
│   └── README_DEV.md
│
└── python/                      # Archived files
```

---

## 🔧 Troubleshooting

### Problem: "Python not found"

**Solution:**
1. Install Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart your terminal/command prompt
4. Try again

### Problem: "pip not found"

**Solution:**
```powershell
python -m ensurepip --upgrade
```

### Problem: "Module not found" errors

**Solution:**
```powershell
pip install -r requirements_file/requirements_dev.txt
```

### Problem: "Port 5000 already in use"

**Solution:**
1. Close any other applications using port 5000
2. Or edit `app_dev.py` line ~700:
   ```python
   app.run(host='0.0.0.0', port=5001, debug=True)
   ```

### Problem: "Database locked"

**Solution:**
1. Close all instances of the application
2. Delete `sentiment_dev.db` file
3. Restart the application (it will create a new database)

### Problem: Scraping returns no results

**Solution:**
1. Try a different URL (see recommended URLs below)
2. Some websites block automated scraping
3. Check your internet connection

---

## 🌐 Recommended URLs for Testing

### ✅ High Success Rate:
```
https://www.bbc.com/news
https://www.reuters.com
https://example.com
https://www.theguardian.com/us
```

### ⚠️ Medium Success Rate:
```
https://techcrunch.com
https://www.wired.com
https://news.ycombinator.com
```

### ❌ Won't Work (Anti-Scraping):
- Amazon
- Facebook
- Twitter/X
- Instagram
- Most e-commerce sites

---

## 📊 Features Overview

### 1. Authentication
- User signup and login
- Secure password hashing
- Session management

### 2. Text Analysis
- Analyze any text for sentiment
- Detects: Positive, Negative, Neutral
- Shows emotion and confidence

### 3. Web Scraping
- Scrape reviews from URLs
- Respects robots.txt
- Automatic deduplication

### 4. Interactive Graph
- Real-time sentiment trends
- Color-coded lines (Green/Red/Orange)
- Filter by sentiment type
- Auto-updates

### 5. Analytics Dashboard
- Total reviews count
- Sentiment distribution
- Average confidence
- Recent reviews feed

---

## 🔒 Security Notes

### For Development:
- ✅ Passwords are hashed (SHA-256)
- ✅ Session-based authentication
- ✅ Input validation
- ✅ SQL injection prevention

### For Production:
When deploying to production, you should:
- Change the SECRET_KEY in `app_dev.py`
- Use HTTPS
- Use a production database (PostgreSQL)
- Add rate limiting
- Enable CORS restrictions

---

## 📝 System Requirements

### Minimum:
- **OS**: Windows 10, macOS 10.14, or Linux
- **Python**: 3.8 or higher
- **RAM**: 512 MB
- **Disk**: 100 MB free space
- **Internet**: Required for scraping

### Recommended:
- **OS**: Windows 11, macOS 12+, or Ubuntu 20.04+
- **Python**: 3.10 or higher
- **RAM**: 1 GB
- **Disk**: 500 MB free space
- **Internet**: Broadband connection

---

## 🎓 Quick Start Commands

### Windows (PowerShell):
```powershell
# Install dependencies
pip install -r requirements_file/requirements_dev.txt

# Run application
python app_dev.py

# Open browser
start http://localhost:5000
```

### Mac/Linux (Terminal):
```bash
# Install dependencies
pip install -r requirements_file/requirements_dev.txt

# Run application
python app_dev.py

# Open browser
open http://localhost:5000  # Mac
xdg-open http://localhost:5000  # Linux
```

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Application starts without errors
- [ ] Browser opens at http://localhost:5000
- [ ] Can create a new account
- [ ] Can login successfully
- [ ] Can analyze text
- [ ] Can scrape a URL (try: https://example.com)
- [ ] Graph displays correctly
- [ ] Can logout

If all checked, you're good to go! 🎉

---

## 📞 Getting Help

### Check Documentation:
1. `README.md` - Project overview
2. `docs/START_HERE.md` - Detailed guide
3. `docs/QUICKSTART.md` - Quick start
4. `requirements_file/SCRAPING_GUIDE.txt` - Scraping help

### Common Issues:
- Check the Troubleshooting section above
- Review console logs for error messages
- Ensure all dependencies are installed
- Try restarting the application

---

## 🎉 Success!

If you can:
1. ✅ Start the application
2. ✅ Create an account
3. ✅ Analyze text
4. ✅ Scrape reviews
5. ✅ See the graph

**Congratulations! Everything is working perfectly!** 🚀

---

## 📦 What's Included

This ZIP file contains:
- ✅ Complete working application
- ✅ All dependencies listed
- ✅ Startup scripts (Windows/Mac/Linux)
- ✅ Comprehensive documentation
- ✅ Sample data for testing
- ✅ No external services required
- ✅ Works offline (except scraping)

---

## 🔄 Updates

To update the project:
1. Download the latest ZIP file
2. Extract to a new folder
3. Copy your `sentiment_dev.db` file (to keep your data)
4. Run the new version

---

**Need more help?** Check the `docs/` folder for detailed guides!

**Ready to start?** Double-click `Bat\START_DEV.bat` (Windows) or run `python app_dev.py`!

🎯 **Happy Analyzing!**
