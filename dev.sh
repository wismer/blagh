#!/bin/bash
# Start both Flask backend and Next.js frontend for local development

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Daily Discover in Hybrid Mode${NC}"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating Python virtual environment..."
    source venv/bin/activate
fi

# Start Flask backend in background
echo -e "${BLUE}Starting Flask backend on port 8080...${NC}"
python run.py &
FLASK_PID=$!

# Wait a moment for Flask to start
sleep 2

# Start Next.js frontend
echo -e "${BLUE}Starting Next.js frontend on port 3000...${NC}"
npm run dev &
NEXT_PID=$!

echo ""
echo -e "${GREEN}✓ Flask API running at http://localhost:8080${NC}"
echo -e "${GREEN}✓ Next.js UI running at http://localhost:3000${NC}"
echo ""
echo "Press CTRL+C to stop both servers"

# Trap CTRL+C and cleanup
trap "kill $FLASK_PID $NEXT_PID; exit" INT

# Wait for both processes
wait
