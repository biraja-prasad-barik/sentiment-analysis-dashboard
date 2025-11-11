# Quick Start Guide

Get the Sentiment Analysis Dashboard running in 3 simple steps!

## 🚀 3-Step Setup

### Step 1: Install Dependencies

```powershell
pip install -r requirements_dev.txt
```

### Step 2: Run the Application

**Option A: Using Python directly**
```powershell
python app_dev.py
```

**Option B: Using the startup script (Windows)**
```powershell
.\START_DEV.bat
```

**Option C: Using PowerShell script**
```powershell
.\START_DEV.ps1
```

### Step 3: Open Dashboard

Open your browser and go to:
```
http://localhost:5000
```

That's it! 🎉

## 📝 What You Can Do

### 1. Analyze Text
- Type or paste text in the "Analyze Text" section
- Click "Analyze Sentiment"
- See sentiment (positive/negative/neutral) and emotion

### 2. Scrape Reviews
- Enter a website URL in the "Scrape Reviews" section
- Set max number of reviews (1-50)
- Click "Scrape & Analyze"
- Reviews will be extracted and analyzed automatically

### 3. View Analytics
- See total reviews count
- View sentiment distribution (positive/negative percentages)
- Check average confidence scores
- Browse recent reviews

## 🧪 Test It Out

Try these sample texts:

**Positive:**
```
This product is absolutely amazing! I love it so much and would highly recommend it to everyone!
```

**Negative:**
```
Terrible experience. The quality is poor and I'm very disappointed with this purchase.
```

**Neutral:**
```
It's an okay product. Does what it's supposed to do, nothing more, nothing less.
```

## 🌐 Try Scraping

Test with these URLs (examples):
- News articles
- Blog posts
- Review sites (that allow scraping)

**Note:** The scraper respects robots.txt and may not work on all websites.

## ❓ Common Questions

### Q: Where is the data stored?
**A:** In a SQLite database file called `sentiment_dev.db` in the project directory.

### Q: Can I reset the database?
**A:** Yes! Just delete `sentiment_dev.db` and restart the app. It will create a fresh database with sample data.

### Q: The scraper isn't finding reviews
**A:** Try different URLs. Some websites block scraping or don't have easily extractable content. The scraper works best with simple HTML pages.

### Q: Can I change the port?
**A:** Yes! Edit `app_dev.py` and change the port number in the last line:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Changed to 5001
```

### Q: How do I stop the server?
**A:** Press `Ctrl+C` in the terminal where the app is running.

## 🐛 Troubleshooting

### "Port 5000 is already in use"
Another application is using port 5000. Either:
- Stop the other application
- Change the port (see above)

### "Module not found" errors
Dependencies not installed. Run:
```powershell
pip install -r requirements_dev.txt
```

### "Database is locked"
Another instance is running. Close it and try again.

### Scraping returns no results
- Check if the URL is accessible
- Try a different website
- Some sites block automated scraping

## 📚 Next Steps

Once you're comfortable with the basics:

1. **Read the full README**: `README_DEV.md`
2. **Run the tests**: `python -m pytest test_dev.py -v`
3. **Explore the API**: Check the API endpoints section in README
4. **Request production features**: When ready, ask for Docker, Celery, etc.

## 💡 Tips

- The app auto-saves all analyzed text and scraped reviews
- Duplicates are automatically detected and skipped
- The dashboard updates automatically after each analysis
- Sample data is added on first run for demo purposes
- All logs are shown in the console for easy debugging

---

**Need help?** Check `README_DEV.md` for detailed documentation!
