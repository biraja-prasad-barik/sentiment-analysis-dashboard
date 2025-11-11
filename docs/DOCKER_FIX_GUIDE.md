# 🔧 Docker Compose Fix Guide

## Issues Identified:

1. ❌ **WSGI/ASGI Mismatch**: Dockerfile uses `uvicorn.workers.UvicornWorker` but Flask needs WSGI
2. ❌ **Database Error**: Postgres healthcheck and connection issues
3. ✅ **Redis**: Working correctly

---

## A) 📝 FIXES TO APPLY

### Fix 1: Update Dockerfile (Remove UvicornWorker)

**File: `Dockerfile`**

**CHANGE THIS LINE (at the end):**
```dockerfile
CMD ["gunicorn", \
     "-w", "4", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "app_production:app", \
     "--bind", "0.0.0.0:5000", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]
```

**TO THIS (WSGI for Flask):**
```dockerfile
CMD ["gunicorn", \
     "-w", "4", \
     "--bind", "0.0.0.0:5000", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "app_production:app"]
```

**OR SIMPLER:**
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app_production:app"]
```

---

### Fix 2: Update docker-compose.yml (Simplify web command)

**File: `docker-compose.yml`**

**CHANGE THIS:**
```yaml
command: ["./wait-for.sh","postgres","5432","gunicorn","--bind","0.0.0.0:5000","app_production:app","-w","4"]
```

**TO THIS:**
```yaml
command: sh -c "./wait-for.sh postgres 5432 && gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 --access-logfile - --error-logfile - app_production:app"
```

---

### Fix 3: Fix Postgres Healthcheck in docker-compose.yml

**CHANGE THIS (in web service):**
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -h postgres -U sentiment_user -d sentiment_prod || exit 1"]
```

**TO THIS:**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/api/v1/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

---

## B) 🔨 COMMANDS TO RUN (Copy-Paste in PowerShell)

### Step 1: Stop All Containers

```powershell
cd "C:\Users\kbari\OneDrive\Desktop\Sentiment Analyzer Project"
docker-compose down
```

**Expected Output:**
```
Stopping sentiment_nginx ... done
Stopping sentiment_web ... done
Stopping sentiment_celery_worker ... done
Stopping sentiment_celery_beat ... done
Stopping sentiment_postgres ... done
Stopping sentiment_redis ... done
Removing containers...
```

---

### Step 2: Fix Database (Create DB if needed)

```powershell
# Start only postgres
docker-compose up -d postgres

# Wait 10 seconds
Start-Sleep -Seconds 10

# Check if database exists
docker exec -it sentiment_postgres psql -U sentiment_user -d sentiment_prod -c "\l"
```

**If you see error "database does not exist":**

```powershell
# The database should already exist from POSTGRES_DB env var
# But if not, create it:
docker exec -it sentiment_postgres psql -U sentiment_user -d postgres -c "CREATE DATABASE sentiment_prod;"
```

**Expected Output:**
```
CREATE DATABASE
```

---

### Step 3: Rebuild and Start All Services

```powershell
# Rebuild images
docker-compose build --no-cache web celery_worker celery_beat

# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

**Expected Output:**
```
NAME                    STATUS              PORTS
sentiment_web           Up (healthy)        0.0.0.0:5000->5000/tcp
sentiment_postgres      Up (healthy)        0.0.0.0:5432->5432/tcp
sentiment_redis         Up (healthy)        0.0.0.0:6379->6379/tcp
sentiment_celery_worker Up                  
sentiment_celery_beat   Up                  
sentiment_nginx         Up                  0.0.0.0:80->80/tcp
```

---

### Step 4: Initialize Database

```powershell
# Wait for web to be healthy (30 seconds)
Start-Sleep -Seconds 30

# Initialize database
docker-compose exec web python scripts/init_db.py
```

**Expected Output:**
```
✅ Database tables created
✅ Default admin user created!
   Email: admin@sentiment.ai
   Password: Admin123!
```

---

### Step 5: View Logs

```powershell
# Check web logs
docker-compose logs --tail=50 web

# Check all logs
docker-compose logs --tail=50
```

**Expected Output (Success):**
```
sentiment_web | [INFO] Booting worker with pid: 7
sentiment_web | [INFO] Listening at: http://0.0.0.0:5000
```

**Should NOT see:**
```
❌ TypeError: Flask.__call__() missing 1 required positional argument
❌ FATAL: database "sentiment_user" does not exist
```

---

## C) ✅ VERIFICATION STEPS

### Test 1: Health Check

```powershell
curl http://localhost:5000/api/v1/health
```

**Expected Output:**
```json
{"status":"healthy","timestamp":"2024-...","service":"sentiment-analysis-api"}
```

---

### Test 2: Detailed Health Check

```powershell
curl http://localhost:5000/api/v1/health/detailed
```

**Expected Output:**
```json
{
  "status":"healthy",
  "checks":{
    "database":{"status":"healthy"},
    "cache":{"status":"healthy"},
    "celery":{"status":"healthy"}
  }
}
```

---

### Test 3: Access Web Interface

```powershell
start http://localhost:5000
```

**Expected:** Login page opens in browser

---

### Test 4: Check Container Health

```powershell
docker-compose ps
```

**Expected:** All containers show "Up (healthy)" or "Up"

---

## D) 🔍 TROUBLESHOOTING COMMANDS

### If Web Container Fails:

```powershell
# Check what files exist in container
docker exec -it sentiment_web ls -la /app

# Check if app_production.py exists
docker exec -it sentiment_web ls -la /app/app_production.py

# Try to import the app
docker exec -it sentiment_web python -c "from app_production import app; print(app)"

# Check environment variables
docker exec -it sentiment_web env | grep DATABASE
```

---

### If Database Connection Fails:

```powershell
# Check database exists
docker exec -it sentiment_postgres psql -U sentiment_user -d sentiment_prod -c "\l"

# Check database connection from web container
docker exec -it sentiment_web python -c "import os; print(os.getenv('DATABASE_URL'))"

# Test connection
docker exec -it sentiment_web python -c "
from sqlalchemy import create_engine
import os
engine = create_engine(os.getenv('DATABASE_URL'))
conn = engine.connect()
print('✅ Database connection successful!')
conn.close()
"
```

---

### If Gunicorn Module Not Found:

```powershell
# Check which app file exists
docker exec -it sentiment_web ls -la /app/*.py | grep app

# Try different module names:
# Option 1: app_production:app
# Option 2: app:app  
# Option 3: app_standalone:app
```

**Update docker-compose.yml command accordingly:**
```yaml
command: sh -c "./wait-for.sh postgres 5432 && gunicorn --bind 0.0.0.0:5000 --workers 4 app:app"
```

---

## E) 📋 QUICK REFERENCE

### Complete Fix Commands (Copy All):

```powershell
# Navigate to project
cd "C:\Users\kbari\OneDrive\Desktop\Sentiment Analyzer Project"

# Stop everything
docker-compose down

# Start postgres only
docker-compose up -d postgres
Start-Sleep -Seconds 10

# Rebuild and start all
docker-compose build --no-cache
docker-compose up -d

# Wait for services
Start-Sleep -Seconds 30

# Initialize database
docker-compose exec web python scripts/init_db.py

# Check status
docker-compose ps

# Test health
curl http://localhost:5000/api/v1/health

# View logs
docker-compose logs --tail=50 web

# Open browser
start http://localhost:5000
```

---

## F) 🎯 EXPECTED SUCCESS INDICATORS

✅ **Web logs show:**
```
[INFO] Booting worker with pid: 7
[INFO] Listening at: http://0.0.0.0:5000
```

✅ **No errors about:**
- `TypeError: Flask.__call__()`
- `FATAL: database ... does not exist`
- `uvicorn.workers.UvicornWorker`

✅ **Health endpoint returns:**
```json
{"status":"healthy"}
```

✅ **Browser shows:** Login page at http://localhost:5000

✅ **Can login with:**
- Email: `admin@sentiment.ai`
- Password: `Admin123!`

---

## G) 🔧 ALTERNATIVE FIXES

### If app_production:app doesn't work:

**Try these in order:**

1. **Check what app files exist:**
```powershell
docker exec -it sentiment_web ls -la /app/*.py | findstr app
```

2. **Try app_standalone.py:**
```yaml
command: sh -c "./wait-for.sh postgres 5432 && gunicorn --bind 0.0.0.0:5000 --workers 4 app_standalone:app"
```

3. **Try app.py:**
```yaml
command: sh -c "./wait-for.sh postgres 5432 && gunicorn --bind 0.0.0.0:5000 --workers 4 app:app"
```

4. **Use create_app factory:**
```yaml
command: sh -c "./wait-for.sh postgres 5432 && gunicorn --bind 0.0.0.0:5000 --workers 4 'app_production:create_app()'"
```

---

## 🎉 SUMMARY

**Main Issues:**
1. Dockerfile uses UvicornWorker (ASGI) instead of WSGI
2. Database connection and healthcheck issues

**Main Fixes:**
1. Remove `-k uvicorn.workers.UvicornWorker` from Dockerfile
2. Simplify docker-compose command
3. Fix healthchecks
4. Ensure database exists

**After fixes, you should have:**
- ✅ Working Flask app on http://localhost:5000
- ✅ Healthy containers
- ✅ No WSGI/ASGI errors
- ✅ Database connected
- ✅ Login page accessible

---

**Need help? Run:**
```powershell
docker-compose logs --tail=100 web
```
