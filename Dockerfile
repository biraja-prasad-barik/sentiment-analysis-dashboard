# ============================================================================
# Multi-stage Production Dockerfile - CPU Only
# Python 3.11 | Flask/FastAPI | Gunicorn + Uvicorn | Non-root user
# ============================================================================

# Stage 1: Builder - Install dependencies
FROM python:3.11-slim as builder

# Set build environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /build

# Copy requirements file (supports multiple formats)
COPY requirements_production.txt* requirements.txt* pyproject.toml* ./

# Install Python dependencies
RUN if [ -f requirements_production.txt ]; then \
        pip install --upgrade pip setuptools wheel && \
        pip install -r requirements_production.txt; \
    elif [ -f requirements.txt ]; then \
        pip install --upgrade pip setuptools wheel && \
        pip install -r requirements.txt; \
    elif [ -f pyproject.toml ]; then \
        pip install --upgrade pip setuptools wheel && \
        pip install .; \
    fi

# Install production server (Gunicorn + Uvicorn)
RUN pip install gunicorn uvicorn[standard]

# ============================================================================
# Stage 2: Runtime - Minimal production image
# ============================================================================
FROM python:3.11-slim

# Set production environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH=/app

# Install only runtime dependencies (no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user and group
RUN groupadd -r app && \
    useradd -r -g app -u 1000 -m -s /sbin/nologin app

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application code with proper ownership
COPY --chown=app:app . .

# Create necessary directories with proper permissions
RUN mkdir -p logs models/cache && \
    chown -R app:app /app && \
    chmod -R 755 /app

# Switch to non-root user
USER app

# Expose application port
EXPOSE 5000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/api/v1/health || exit 1

# Run application with Gunicorn (WSGI for Flask - NO UvicornWorker)
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "4", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "app_production:app"]
