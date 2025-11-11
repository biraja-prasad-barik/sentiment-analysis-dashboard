#!/bin/bash
# Start development environment

echo "Starting development environment..."

# Check if Redis is running
if ! redis-cli ping > /dev/null 2>&1; then
    echo "❌ Redis is not running. Please start Redis first."
    echo "   Windows: Start Redis from Services"
    echo "   Linux: sudo service redis-server start"
    exit 1
fi

# Start Celery worker in background
echo "Starting Celery worker..."
celery -A core.celery_app worker --loglevel=info &
CELERY_PID=$!

# Start Celery beat in background
echo "Starting Celery beat..."
celery -A core.celery_app beat --loglevel=info &
BEAT_PID=$!

# Start Flask app
echo "Starting Flask application..."
export FLASK_ENV=development
python app_production.py

# Cleanup on exit
trap "kill $CELERY_PID $BEAT_PID" EXIT
