#!/bin/bash
# Start both Flask backend and Next.js frontend for local development

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Daily Discover (Flask + Pelican)${NC}"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating Python virtual environment..."
    source venv/bin/activate
fi

# Start Flask
echo -e "${BLUE}Starting Flask on port 8080...${NC}"
python run.py &
FLASK_PID=$!

echo ""
echo -e "${GREEN}✓ Flask running at http://localhost:8080${NC}"
echo -e "${GREEN}✓ Dashboard at http://localhost:8080/dashboard${NC}"
echo -e "${GREEN}✓ API at http://localhost:8080/api/health${NC}"
echo ""
echo "Blog development: Run 'pelican --listen -r' in another terminal"
echo ""
echo "Press CTRL+C to stop server"

# Trap CTRL+C and cleanup
trap "kill $FLASK_PID; exit" INT

# Wait for both processes
wait
