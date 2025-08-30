# Scenario API - FastAPI Makefile
# Useful commands for development, testing, and deployment

.PHONY: help install dev dev-logs dev-stop staging staging-stop prod prod-stop test lint lint-fix migrate migrate-create restore-db shell db-shell push clean

# Default target
help:
	@echo "🎬 Scenario API - Available Commands"
	@echo "=================================="
	@echo "📦 Setup & Installation:"
	@echo "  install       - Install Python dependencies"
	@echo "  clean         - Clean Python cache files"
	@echo ""
	@echo "🚀 Development:"
	@echo "  dev           - Start development environment"
	@echo "  dev-logs      - View development logs"
	@echo "  dev-stop      - Stop development environment"
	@echo ""
	@echo "🎯 Testing & Quality:"
	@echo "  test          - Run tests with coverage"
	@echo "  test-watch    - Run tests in watch mode"
	@echo "  lint          - Check code with pylint"
	@echo "  lint-fix      - Auto-fix code issues"
	@echo ""
	@echo "🗄️ Database:"
	@echo "  migrate       - Apply database migrations"
	@echo "  migrate-create - Create new migration"
	@echo "  restore-db    - Restore database from SQL dump"
	@echo "  db-shell      - Open PostgreSQL shell"
	@echo ""
	@echo "🐳 Deployment:"
	@echo "  staging       - Start staging environment"
	@echo "  staging-stop  - Stop staging environment"
	@echo "  prod          - Start production environment"
	@echo "  prod-stop     - Stop production environment"
	@echo "  push          - Build and push Docker images"
	@echo ""
	@echo "🔧 Utilities:"
	@echo "  shell         - Open shell in API container"
	@echo "  logs-dev      - View development logs"
	@echo "  logs-prod     - View production logs"

# Setup & Installation
install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt

clean:
	@echo "🧹 Cleaning Python cache files..."
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# Development Environment
dev:
	@echo "🚀 Starting development environment..."
	docker-compose -f docker-compose.dev.yaml up -d

dev-logs:
	@echo "📋 Viewing development logs..."
	docker-compose -f docker-compose.dev.yaml logs -f

dev-stop:
	@echo "🛑 Stopping development environment..."
	docker-compose -f docker-compose.dev.yaml down

# Testing & Quality
test:
	@echo "🧪 Running tests with coverage..."
	pytest --cov=app --cov-report=term --cov-report=html

test-watch:
	@echo "👀 Running tests in watch mode..."
	pytest-watch --runner "pytest --cov=app"

lint:
	@echo "🔍 Checking code with pylint..."
	pylint app/

lint-fix:
	@echo "🔧 Auto-fixing code issues..."
	black app/
	isort app/

# Database Management
migrate:
	@echo "🗄️ Applying database migrations..."
	alembic upgrade head

migrate-create:
	@echo "📝 Creating new migration..."
	@read -p "Enter migration name: " name; \
	alembic revision --autogenerate -m "$$name"

restore-db:
	@echo "🔄 Starting database restore..."
	python app/database/restore_data.py

db-shell:
	@echo "🐘 Opening PostgreSQL shell..."
	docker-compose -f docker-compose.dev.yaml exec scenario-postgres \
		psql -U scenario_user -d scenario_db

# Staging Environment
staging:
	@echo "🎯 Starting staging environment..."
	docker-compose -f docker-compose.staging.yaml up -d

staging-stop:
	@echo "🛑 Stopping staging environment..."
	docker-compose -f docker-compose.staging.yaml down

# Production Environment
prod:
	@echo "🚀 Starting production environment..."
	docker-compose -f docker-compose.prod.yaml up -d

prod-stop:
	@echo "🛑 Stopping production environment..."
	docker-compose -f docker-compose.prod.yaml down

# Docker Image Management
push:
	@echo "📦 Building and pushing Docker images..."
	docker build -t $(DOCKER_REGISTRY)/scenario-api:latest .
	docker push $(DOCKER_REGISTRY)/scenario-api:latest

# Utilities
shell:
	@echo "🐚 Opening shell in API container..."
	docker-compose -f docker-compose.dev.yaml exec scenario-api /bin/sh

logs-dev:
	@echo "📋 Viewing development logs..."
	docker-compose -f docker-compose.dev.yaml logs -f scenario-api

logs-prod:
	@echo "📋 Viewing production logs..."
	docker-compose -f docker-compose.prod.yaml logs -f scenario-api

# Environment Setup
setup-dev:
	@echo "⚙️ Setting up development environment..."
	cp .env.example .env
	@echo "✅ Don't forget to edit .env with your configuration!"

# Health Checks
check-health:
	@echo "🩺 Checking API health..."
	curl -f http://localhost:8000/health || echo "❌ API is not responding"

# Database Backup (create dump)
backup-db:
	@echo "💾 Creating database backup..."
	@mkdir -p app/database/backup
	docker-compose -f docker-compose.dev.yaml exec scenario-postgres \
		pg_dump -U scenario_user scenario_db > app/database/backup/scenario_dump_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created in app/database/backup/"