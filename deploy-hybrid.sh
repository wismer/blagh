#!/bin/bash
# Production deployment script for Raspberry Pi

set -e  # Exit on error
set -o pipefail  # Catch errors in pipes

# Error handler - shows which command failed
trap 'echo "❌ Error on line $LINENO: $BASH_COMMAND" >&2' ERR

echo "🚀 Deploying Daily Discover (Flask + Pelican)"
echo ""

# 1. Update code
echo "📦 Pulling latest code..."
git pull

# 2. Install Python dependencies
echo "🐍 Installing Python dependencies..."
uv pip install -r requirements.txt
uv pip install -r requirements-prod.txt

# 3. Build Pelican blog
echo "📝 Building static blog with Pelican..."
pelican posts/ -o static/blog -s pelicanconf.py

# 4. Run database migrations if schema changed
echo "🗄️  Checking database..."
# Uncomment if you have migrations:
# psql $DATABASE_URL < schema.sql

# 5. Restart Flask service
echo "🔄 Restarting Flask service..."

# Copy updated service file
sudo cp systemd/daily-discover-flask.service /etc/systemd/system/
sudo systemctl daemon-reload

# Restart Flask
sudo systemctl restart daily-discover-flask

# 6. Verify
echo ""
echo "✅ Deployment complete!"
echo "Flask API & Web: http://localhost:8080"
echo "Blog: http://localhost:8080/blog"
