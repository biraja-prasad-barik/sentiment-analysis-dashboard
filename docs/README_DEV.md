# Sentiment Analysis Dashboard - Development Version

A simple, stable sentiment analysis dashboard for collecting and analyzing reviews from the web.

**Note:** This is the development version. Production features (Docker, Celery, Redis, PostgreSQL, monitoring, etc.) have been **intentionally removed** and will be added later when requested.

## 🎯 Features

- **Simple Flask Backend**: Single-process application, no complex infrastructure
- **SQLite Database**: Local file-based storage, no external database servers
- **Web Scraping**: Polite scraper that respects robots.txt
- **Sentiment Analysis**: Lightweight keyword-based model (no heavy ML dependencies)
- **Deduplication**: Automatic detection and skipping of duplicate reviews
- **Clean Frontend**: Minimal HTML/CSS/JS dashboard
- **RESTful API**: Simple endpoints for all operations

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
pip install -r requirements_dev.txt
```

### 2. Run the Application

```powershell
python app_dev.py
```

### 3. Open Dashboard

Open your browser and navigate to:
```
http://localhost:5000
```

That's it! The application will:
- Create the SQLite database automatically
- Add sample data for demo purposes
- Start the Flask development server

## 📁 Project Structure

```
.
├── app_dev.py              # Main application file
├── requirements_dev.txt    # Python dependencies
├── test_dev.py            # Unit tests
├── static/
│   └── index.html         # Frontend dashboard
└── sentiment_dev.db       # SQLite database (created automatically)
```

## 🔌 API Endpoints

### Health Check
```
GET /api/health
```
Returns server status and basic info.

### Analyze Text
```
POST /api/analyze
Content-Type: application/json

{
  "text": "This product is amazing!"
}
```
Analyzes sentiment and emotion of provided text.

### Scrape Reviews
```
POST /api/scrape
Content-Type: application/json

{
  "url": "https://example.com",
  "max_reviews": 10
}
```
Scrapes reviews from a URL and analyzes them.

### Get Reviews
```
GET /api/reviews?page=1&per_page=20
```
Returns paginated list of reviews.

### Dashboard Data
```
GET /api/dashboard
```
Returns analytics data for the dashboard.

## 🧪 Running Tests

```powershell
# Install pytest if not already installed
pip install pytest

# Run tests
python -m pytest test_dev.py -v
```

## 🔧 Configuration

The application uses sensible defaults for development:

- **Host**: `0.0.0.0` (accessible from network)
- **Port**: `5000`
- **Database**: `sqlite:///sentiment_dev.db`
- **Debug Mode**: `True`

To change these, edit the configuration section in `app_dev.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentiment_dev.db'
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
```

## 📊 How It Works

### Sentiment Analysis

The application uses a lightweight keyword-based approach:

1. **Preprocessing**: Text is cleaned and normalized
2. **Keyword Matching**: Positive and negative keywords are counted
3. **Sentiment Classification**: Based on keyword counts
4. **Emotion Detection**: Identifies primary emotion from text
5. **Confidence Score**: Calculated based on keyword strength

This approach is:
- Fast and lightweight (no heavy ML models)
- Reliable for basic sentiment analysis
- Easy to understand and debug
- No GPU or large memory requirements

### Web Scraping

The scraper:
1. Checks `robots.txt` to respect website policies
2. Fetches HTML content with proper user agent
3. Extracts text from common review selectors
4. Filters content by reasonable length (20-2000 chars)
5. Returns clean text for analysis

### Deduplication

Reviews are deduplicated using SHA-256 hashes:
- Each review text is hashed
- Hash is stored in database with unique constraint
- Duplicate reviews are detected and skipped
- Prevents redundant storage and analysis

## 🎨 Frontend Features

The dashboard provides:

- **Analytics Overview**: Total reviews, sentiment distribution, confidence scores
- **Text Analysis**: Manual text input for instant analysis
- **Web Scraping**: URL-based review collection
- **Recent Reviews**: Live feed of analyzed reviews
- **Responsive Design**: Works on desktop and mobile

## 🐛 Troubleshooting

### Port Already in Use

If port 5000 is already in use, change it in `app_dev.py`:

```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Database Locked

If you get "database is locked" errors:
1. Close any other instances of the application
2. Delete `sentiment_dev.db` and restart

### Scraping Fails

If scraping doesn't work:
1. Check if the website allows scraping (robots.txt)
2. Verify the URL is accessible
3. Some websites may block automated requests
4. Try a different URL

### Import Errors

Make sure all dependencies are installed:

```powershell
pip install -r requirements_dev.txt
```

## 📝 Development Notes

### Why No Heavy ML Models?

This development version uses a lightweight keyword-based approach instead of transformer models (BERT, RoBERTa, etc.) because:

- **Fast startup**: No model loading time
- **Low memory**: Runs on any machine
- **Easy debugging**: Simple logic to understand
- **Sufficient accuracy**: Good enough for development and testing

### Why SQLite?

SQLite is perfect for development:

- **No setup**: Works out of the box
- **File-based**: Easy to backup and reset
- **Portable**: Database is just a file
- **Fast enough**: Handles thousands of reviews easily

### Why No Docker?

Docker adds complexity that's not needed for development:

- **Slower startup**: Container build and startup time
- **More dependencies**: Docker Desktop, docker-compose
- **Harder debugging**: Extra layer of abstraction
- **Overkill**: Not needed for local development

## 🚀 Adding Production Features

When you're ready for production, request these features:

- **Docker**: Containerization with docker-compose
- **PostgreSQL**: Production-grade database
- **Celery + Redis**: Background task processing
- **Scheduled Scraping**: Automatic periodic scraping
- **Advanced ML**: Transformer-based models (BERT, RoBERTa)
- **Monitoring**: Logging, metrics, health checks
- **Authentication**: User management and API keys
- **Rate Limiting**: API throttling and quotas
- **Caching**: Redis-based response caching
- **Load Balancing**: Multiple worker processes
- **CI/CD**: Automated testing and deployment

## 📄 License

See LICENSE file for details.

## 🤝 Contributing

This is a development version. For production features, please request them explicitly.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments in `app_dev.py`
3. Run tests to verify functionality
4. Check logs for error messages

---

**Remember**: This is intentionally simple. Production features will be added when you request them!
