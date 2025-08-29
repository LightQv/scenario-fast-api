# SCENARIO API - FastAPI Version

Welcome to the FastAPI version of the Scenario API! A modern API for managing your watchlists and tracking your movie and TV show viewing history.

## 🚀 Technologies

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

## 📋 Features

- ✅ **Complete Authentication**: Registration, login, forgot password
- 🎬 **Watchlist Management**: Create, edit, delete your movie/TV lists
- 👁️ **Viewing History**: Track what you've watched
- 📊 **Statistics**: Analyze your viewing habits
- 🔐 **Security**: JWT with HTTPOnly cookies, bcrypt hashing
- 📧 **Email System**: Password reset with fastapi-mail
- 🐳 **Multi-environments**: Dev, Staging, Production with Docker
- 🔍 **Monitoring**: Logging with Loguru, error tracking with Sentry

## 🏗️ Architecture

```
app/
├── core/              # Configuration, database, security
├── models/            # SQLAlchemy models
├── schemas/           # Pydantic schemas
├── api/v1/            # API routes
├── services/          # Business logic
├── utils/             # Utilities (email templates, etc.)
└── database/          # Database configuration and tools
    ├── backup/        # SQL dump files
    └── restore_data.py # Database restore script
```

## 🚀 Quick Start

### With Makefile (Recommended)

```bash
# Clone the repository
git clone <your-repo>
cd scenario-fastapi

# Copy and configure environment
cp .env.example .env
# Edit the .env file

# Start development environment
make dev

# View logs
make dev-logs

# Stop environment
make dev-stop
```

### Manual Installation

1. **Prerequisites**
   - Python 3.12+
   - PostgreSQL
   - Docker and Docker Compose

2. **Installation**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
make install
# or pip install -r requirements.txt

# Configuration
cp .env.example .env
```

3. **Database**
```bash
# With Docker
make dev

# Or manually
alembic upgrade head
```

## 🗄️ Database Management

### Database Restore from Supabase Dump

If you have a SQL dump from Supabase or another PostgreSQL database, you can restore it using our restore tool.

#### Setup

1. **Place your SQL dump file** in `app/database/backup/scenario_dump.sql`
2. **Make sure PostgreSQL client is installed** (`psql` command must be available)

#### Restore Database

⚠️ **WARNING: This operation will completely replace your current database!**

```bash
# Restore from default dump file (app/database/backup/scenario_dump.sql)
make restore-db
# or
python app/database/restore_data.py

# Restore from custom dump file
python app/database/restore_data.py /path/to/your/dump.sql
```

The script will:
- Ask for confirmation (this operation is **irreversible**)
- Drop all existing data
- Restore from the SQL dump file
- Show progress and results

#### Example Restore Session

```bash
$ make restore-db

🔄 Scenario API - Database Restore Tool
========================================
⚠️  WARNING: DATABASE RESTORE OPERATION
==================================================
This operation will:
• DROP all existing tables and data
• RESTORE from the SQL dump file
• This action is IRREVERSIBLE
==================================================
Are you sure you want to continue? (y/N): y

✅ Database restore completed successfully!
```

## 🐳 Docker Environments

### Development
```bash
make dev              # Start
make dev-logs         # View logs  
make dev-stop         # Stop
```
- API: http://localhost:8000
- Adminer: http://localhost:8080
- Hot reload enabled

### Staging
```bash
make staging          # Start
make staging-stop     # Stop
```
- API with Nginx: http://localhost:8001
- Rate limiting enabled
- Enhanced security

### Production
```bash
make prod             # Start
make prod-stop        # Stop
```
- HTTPS with SSL
- Aggressive rate limiting
- Complete monitoring

## 📦 Deployment with Docker Images

### Build and Push to DockerHub

```bash
# Configure registry
export DOCKER_REGISTRY=your-dockerhub-username

# Build and push
make push

# Or with deployment script
chmod +x scripts/deploy.sh
./scripts/deploy.sh --environment prod --registry your-dockerhub-username
```

### Using Images in Production

```bash
# Modify docker-compose.prod.yaml
services:
  scenario-api:
    image: your-dockerhub-username/scenario-api:latest
    # ...
```

## 🔧 Environment Variables

### Development (.env)
```env
APP_NAME="Scenario API"
DEBUG=true
DATABASE_URL="postgresql://scenario_user:scenario_password@localhost:5432/scenario_db"
JWT_SECRET_KEY="your_dev_secret"
FRONTEND_URL="http://localhost:3000"
```

### Production (.env.prod)
```env
APP_NAME="Scenario API"
DEBUG=false
DATABASE_URL="postgresql://prod_user:strong_password@scenario-postgres:5432/scenario_prod_db"
JWT_SECRET_KEY="very_long_and_secure_production_key"
FRONTEND_URL="https://scenario.yourdomain.com"
SENTRY_DSN="https://your-sentry-dsn@sentry.io/project-id"
```

## 📚 API Documentation

- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`

## 🛠️ Useful Commands

```bash
# Tests
make test             # Run tests
pytest --cov=app     # Tests with coverage

# Linting
make lint             # Check code
make lint-fix         # Auto-fix issues

# Database
make migrate          # Apply migrations
make migrate-create   # Create new migration
make restore-db       # Restore from SQL dump

# Logs
make logs-dev         # Development logs
make logs-prod        # Production logs

# Debug
make shell            # Shell in container
make db-shell         # PostgreSQL shell
```

## 🔍 Monitoring and Observability

### Logs with Loguru
```python
from loguru import logger

logger.info("User logged in", user_id=user.id)
logger.error("Database connection failed", error=str(e))
```

### Error Tracking with Sentry
```python
# Automatic with FastAPI integration
# Configured in app/main.py
```

### Nginx Metrics
- Detailed logs with response times
- Rate limiting per endpoint
- Security headers

## 🚨 Security

### Security Headers (Nginx)
- `Strict-Transport-Security`
- `X-Frame-Options`
- `X-XSS-Protection`
- `Content-Security-Policy`

### Rate Limiting
- Auth endpoints: 10 req/s
- General API: 30 req/s (prod), 10 req/s (staging)
- Burst allowing traffic spikes

### Authentication
- JWT with HTTPOnly cookies
- Bcrypt for password hashing
- Secure reset tokens
- Strict input validation with Pydantic

## 🧪 Tests

```bash
# Run all tests
make test

# Tests with detailed coverage
pytest --cov=app --cov-report=html
open htmlcov/index.html

# Tests in watch mode (development)
make test-watch

# Test specific module
pytest tests/test_auth.py -v
```

## 📁 Docker File Structure

```
├── Dockerfile              # Production (multi-stage)
├── Dockerfile.dev          # Development
├── docker-compose.dev.yaml # Dev environment
├── docker-compose.staging.yaml # Staging environment  
├── docker-compose.prod.yaml # Production environment
├── nginx/
│   ├── nginx.dev.conf      # Nginx dev config
│   ├── nginx.staging.conf  # Nginx staging config
│   └── nginx.prod.conf     # Nginx prod config
├── scripts/
│   └── deploy.sh           # Deployment script
└── Makefile                # Useful commands
```

## 🔄 Deployment Workflow

### 1. Local Development
```bash
# Develop locally with hot reload
make dev
```

### 2. Testing and Validation
```bash
# Unit tests
make test

# Code checking
make lint
```

### 3. Staging Deployment
```bash
# Build and deploy to staging
./scripts/deploy.sh --environment staging
```

### 4. Production Deployment
```bash
# Build, push to DockerHub and deploy
./scripts/deploy.sh --environment prod --registry your-dockerhub-username
```

## 🌐 SSL/HTTPS Configuration (Production)

### 1. Let's Encrypt Certificates
```bash
# Create certificates directory
mkdir -p certs

# Get certificates (with certbot)
certbot certonly --webroot -w /var/www/certbot -d yourdomain.com
```

### 2. Automatic Renewal
```bash
# Add to crontab
0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Advanced Monitoring

### Health Checks
- `/health` endpoint to check API status
- Docker health checks for containers
- Database monitoring

### Custom Metrics
```python
# In your endpoints
from loguru import logger
import time

@router.post("/example")
def example_endpoint():
    start_time = time.time()
    # ... business logic
    duration = time.time() - start_time
    logger.info("Endpoint executed", endpoint="example", duration=duration)
```

## 🔧 Advanced Configuration

### Environment Variables by Service

#### Database
```env
POSTGRES_DB=scenario_db
POSTGRES_USER=scenario_user  
POSTGRES_PASSWORD=secure_password
```

#### Email (Gmail with app password)
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_specific_password
SMTP_USE_TLS=true
```

#### Sentry (Error Monitoring)
```env
SENTRY_DSN=https://your_key@sentry.io/project_id
```

## 🚀 Performance Optimizations

### Database
- Indexes on frequently queried columns
- Connection pooling with SQLAlchemy
- Optimized queries with joins

### Application
- HTTP connection reuse with `httpx`
- Database session caching
- Optimized Pydantic validation

### Infrastructure
- Nginx as reverse proxy
- Gzip compression
- Keep-alive connections
- Buffer optimization

## 🔍 Debugging

### Development Logs
```bash
# View logs in real-time
make dev-logs

# Logs from specific service
docker-compose -f docker-compose.dev.yaml logs -f scenario-api
```

### Container Access
```bash
# Shell in API container
make shell

# PostgreSQL shell
make db-shell

# Inspect database
docker-compose -f docker-compose.dev.yaml exec scenario-postgres \
  psql -U scenario_user -d scenario_db -c "SELECT * FROM user_model LIMIT 5;"
```

## 📈 Migration from Express

### Existing Data
```bash
# SQLAlchemy models are compatible with your Express schema
# No data migration needed if using the same DB
```

### API Changes
- Routes prefixed with `/api/v1/`
- Normalized JSON responses
- Automatic input validation
- Automatic documentation

### Frontend
```javascript
// Old (Express)
const response = await fetch('/auth/login', { ... })

// New (FastAPI)  
const response = await fetch('/api/v1/auth/login', { ... })
```

## 🤝 Contributing

### Code Standards
- PEP 8 for Python style
- Docstrings for all public functions
- Type hints required
- Unit tests for new features

### Workflow
1. Fork the project
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Follow standards (`make lint`)
4. Add tests (`make test`)
5. Commit with clear messages
6. Open Pull Request

## 📄 License

This project is licensed under the ISC License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support and FAQ

### Common Issues

**Port already in use**
```bash
# Check used ports
lsof -i :8000

# Or change port in .env
APP_PORT=8001
```

**Database connection issue**
```bash
# Check PostgreSQL is running
make dev-logs

# Recreate volumes if needed
docker-compose -f docker-compose.dev.yaml down -v
make dev
```

**SSL errors in production**
```bash
# Check certificates
docker-compose -f docker-compose.prod.yaml exec scenario-nginx \
  openssl x509 -in /etc/nginx/certs/fullchain.pem -text -noout
```

**Database restore fails**
```bash
# Check PostgreSQL client is installed
which psql

# Check dump file format
head -n 10 app/database/backup/scenario_dump.sql

# Check database connection
psql $DATABASE_URL -c "SELECT version();"
```

### Useful Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Developed with ❤️ in FastAPI by [Your Name]**

🔗 **Useful Links:**
- API Docs: `http://localhost:8000/docs`
- Adminer: `http://localhost:8080` 
- Monitoring: Configure Sentry for production monitoring