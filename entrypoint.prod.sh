#!/bin/sh

echo "🚀 Starting Scenario API (Production)"

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
while ! nc -z scenario-postgres 5432; do
    sleep 1
done
echo "✅ Database is ready!"

# Run database migrations
echo "📝 Running database migrations..."
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "✅ Migrations completed successfully"
else
    echo "❌ Migration failed"
    exit 1
fi

# Start the application
echo "🏃 Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000