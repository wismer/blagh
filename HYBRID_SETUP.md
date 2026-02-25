# Hybrid Architecture Setup Guide

## Architecture Overview

**Daily Discover** uses a hybrid architecture:
- **Flask Backend** (port 8080): Python APIs, Gmail integration, database operations
- **Next.js Frontend** (port 3000): TypeScript UI, static generation, client routing

### Why Hybrid?

- **Flask**: Lightweight, efficient for Pi, excellent Python ecosystem (Gmail API, PostgreSQL)
- **Next.js**: Modern React framework, TypeScript safety, static export capability
- **Best of both**: Python for heavy lifting, JavaScript for UI

---

## Local Development

### Prerequisites

```bash
# Python 3.10+
python --version

# Node.js 18+
node --version

# PostgreSQL running
psql --version
```

### Setup

1. **Clone and enter directory**
```bash
git clone <your-repo>
cd daily-discover
```

2. **Set up Python environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Set up Node environment**
```bash
npm install
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your values:
# - DATABASE_URL
# - GMAIL_CLIENT_ID
# - GMAIL_CLIENT_SECRET
# - SECRET_KEY
```

5. **Initialize database**
```bash
psql -U matt -d daily_discover < schema.sql
```

### Run Development Servers

**Option 1: Automatic (both servers)**
```bash
chmod +x dev.sh
./dev.sh
```

**Option 2: Manual (separate terminals)**

Terminal 1 - Flask:
```bash
source venv/bin/activate
python run.py
# Flask runs on http://localhost:8080
```

Terminal 2 - Next.js:
```bash
npm run dev
# Next.js runs on http://localhost:3000
```

**Access the app:**
- UI: http://localhost:3000
- API: http://localhost:8080/api/health

---

## Production Deployment (Raspberry Pi)

### Initial Setup

1. **Install system dependencies**
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv nodejs npm postgresql
```

2. **Clone repository**
```bash
cd /home/pi
git clone <your-repo> daily-discover
cd daily-discover
```

3. **Set up Python**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-prod.txt
```

4. **Set up Node**
```bash
npm install
npm run build
```

5. **Configure systemd services**
```bash
sudo cp systemd/*.service /etc/systemd/system/
sudo mkdir -p /var/log/daily-discover
sudo chown pi:pi /var/log/daily-discover

# Update paths in service files if needed
sudo nano /etc/systemd/system/daily-discover-flask.service
sudo nano /etc/systemd/system/daily-discover-next.service

sudo systemctl daemon-reload
sudo systemctl enable daily-discover-flask
sudo systemctl enable daily-discover-next
```

6. **Start services**
```bash
sudo systemctl start daily-discover-flask
sudo systemctl start daily-discover-next

# Check status
sudo systemctl status daily-discover-flask
sudo systemctl status daily-discover-next
```

### Deploy Updates

```bash
chmod +x deploy-hybrid.sh
./deploy-hybrid.sh
```

---

## Cloudflare Integration

### Option 1: Cloudflare Tunnel (Recommended)

**Why?** No port forwarding, automatic HTTPS, DDoS protection, hides home IP.

1. **Install cloudflared**
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
sudo dpkg -i cloudflared-linux-arm64.deb
```

2. **Authenticate**
```bash
cloudflared tunnel login
```

3. **Create tunnel**
```bash
cloudflared tunnel create daily-discover
cloudflared tunnel route dns daily-discover yourdomain.com
```

4. **Configure tunnel**
```bash
cat > ~/.cloudflared/config.yml << EOF
tunnel: <TUNNEL-ID>
credentials-file: /home/pi/.cloudflared/<TUNNEL-ID>.json

ingress:
  - hostname: yourdomain.com
    service: http://localhost:3000
  - hostname: api.yourdomain.com
    service: http://localhost:8080
  - service: http_status:404
EOF
```

5. **Run tunnel as service**
```bash
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

### Option 2: Traditional DNS + Cloudflare Proxy

1. Point DNS A record to your public IP
2. Enable Cloudflare proxy (orange cloud)
3. Set up Page Rules (free tier gets 3):
   - `yourdomain.com/*` → Cache Level: Standard
   - `yourdomain.com/_next/static/*` → Cache Level: Cache Everything
   - `api.yourdomain.com/*` → Cache Level: Bypass

### Caching Strategy

Add to [next.config.js](next.config.js):
```javascript
async headers() {
  return [
    {
      source: '/_next/static/:path*',
      headers: [
        { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' }
      ]
    },
    {
      source: '/posts/:path*',
      headers: [
        { key: 'Cache-Control', value: 'public, s-maxage=3600, stale-while-revalidate=86400' }
      ]
    }
  ];
}
```

---

## Architecture Decisions

### Why Flask for Backend?

- **Memory**: 50-100MB vs 200-500MB for Node
- **Python ecosystem**: Gmail API, database libraries
- **Simplicity**: Single Gunicorn process
- **Pi-friendly**: Lower resource usage

### Why Next.js for Frontend?

- **Modern DX**: Hot reload, TypeScript, built-in routing
- **Static export**: Deploy to Cloudflare Pages (optional)
- **Performance**: Automatic code splitting, image optimization
- **SEO**: Server-side rendering capability

### API Communication

- **Development**: Next.js rewrites `/api/*` to Flask on port 8080
- **Production**: Both run on Pi, Next.js proxies internally
- **Alternative**: Deploy Next.js to Cloudflare Pages, tunnel API calls to Pi

---

## Troubleshooting

### Flask won't start
```bash
# Check logs
sudo journalctl -u daily-discover-flask -f

# Test manually
source venv/bin/activate
python run.py
```

### Next.js can't connect to API
```bash
# Verify Flask is running
curl http://localhost:8080/api/health

# Check CORS in app.py
# Ensure localhost:3000 is in allowed origins
```

### Port already in use
```bash
# Find process
lsof -i :8080
lsof -i :3000

# Kill if needed
kill -9 <PID>
```

### Database connection issues
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify connection
psql -U matt -d daily_discover -c "SELECT 1;"
```

---

## Performance Tips for Pi

1. **Use gunicorn workers wisely**: 2-4 workers max on Pi 4
2. **Enable Cloudflare caching**: Reduces load on Pi
3. **Static assets**: Serve from Cloudflare CDN
4. **Database indexing**: Ensure proper indexes on frequently queried columns
5. **Log rotation**: Set up logrotate for `/var/log/daily-discover/`

---

## Future Enhancements

- [ ] Move Next.js static export to Cloudflare Pages (free)
- [ ] Use Cloudflare Workers for API caching layer
- [ ] Set up automated backups
- [ ] Add monitoring (Uptime Robot, Grafana)
- [ ] Redis caching for frequently accessed data
