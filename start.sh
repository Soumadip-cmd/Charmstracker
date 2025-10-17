#!/bin/bash

# CharmTracker Backend Startup Script for Hostinger
# Make this executable with: chmod +x start.sh

echo "🚀 Starting CharmTracker Backend..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies if requirements.txt exists
if [ -f "backend/requirements.txt" ]; then
    echo "📥 Installing dependencies..."
    pip install -r backend/requirements.txt
fi

# Navigate to backend directory
cd backend

# Start the FastAPI application with Uvicorn
echo "🌐 Starting Uvicorn server..."
uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000} --workers 4

# Alternative: Use Gunicorn for production
# gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000}
