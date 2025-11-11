#!/bin/bash
# Run tests with coverage

echo "Running tests..."

# Set test environment
export FLASK_ENV=testing

# Run pytest with coverage
pytest tests/ \
    --cov=. \
    --cov-report=html \
    --cov-report=term-missing \
    --verbose

echo ""
echo "Coverage report generated in htmlcov/index.html"
