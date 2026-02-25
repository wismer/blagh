#!/bin/bash
# Production deployment script for Raspberry Pi

set -e  # Exit on error

echo "🚀 Deploying Daily Discover (Hybrid Mode)"
echo ""

# 1. Update code
echo "📦 Pulling latest code..."
git pull

# 2. Install Python dependencies
echo "🐍 Installing Python dependencies..."
source .venv/bin/activate
uv install -r requirements.txt
uv install -r requirements-prod.txt

# 3. Install Node dependencies and build Next.js
echo "📦 Installing Node dependencies..."
npm install

echo "🏗️  Building Next.js..."
npm run build

# 4. Run database migrations if schema changed
echo "🗄️  Checking database..."
# Uncomment if you have migrations:
# psql $DATABASE_URL < schema.sql

# 5. Restart services
echo "🔄 Restarting services..."

# Stop existing services
sudo systemctl stop daily-discover-flask 2>/dev/null || true
sudo systemctl stop daily-discover-next 2>/dev/null || true

# Start Flask with Gunicorn
echo "▶️  Starting Flask backend..."
sudo systemctl start daily-discover-flask

# Start Next.js
echo "▶️  Starting Next.js frontend..."
sudo systemctl start daily-discover-next

# 6. Verify
echo ""
echo "✅ Deployment complete!"
echo "Flask API: http://localhost:8080/api/health"
echo "Next.js UI: http://localhost:3000"
