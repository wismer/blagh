# Daily Discover - Flask + Pelican Setup

## Architecture

**Daily Discover** is a personal dashboard with a static blog:
- **Flask** (port 8080): Python web server, APIs, dashboard
- **Pelican**: Static blog generation from Markdown
- **PostgreSQL**: Database for todos, groceries, activity logs

## Local Development

### Prerequisites

```bash
python --version  # 3.10+
psql --version    # PostgreSQL
```

### Setup

1. **Clone and setup**
```bash
git clone <your-repo>
cd daily-discover
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your DATABASE_URL, GMAIL credentials, SECRET_KEY
```

3. **Initialize database**
```bash
psql -U matt -d daily_discover < schema.sql
```

4. **Build blog**
```bash
pelican posts/ -o static/blog -s pelicanconf.py
```

5. **Run Flask**
```bash
python run.py
# Visit http://localhost:8080
```

Or use the dev script:
```bash
./dev.sh
```

## Production Deployment (Raspberry Pi)

### Initial Setup

1. **Install dependencies**
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv postgresql
```

2. **Clone and setup**
```bash
cd /home/gremlin
git clone <your-repo> blagh
cd blagh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-prod.txt
```

3. **Install uv (optional, faster)**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

4. **Configure systemd**
```bash
sudo cp systemd/daily-discover-flask.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable daily-discover-flask
sudo systemctl start daily-discover-flask
```

### Deploy Updates

```bash
./deploy-hybrid.sh
```

This script:
- Pulls latest code
- Installs Python dependencies
- Rebuilds Pelican blog
- Restarts Flask service

## Routes

**Public (Blog):**
- `/` → Blog index
- `/blog/2026-02-24/welcome.html` → Blog posts
- `/pages/about.html` → Static pages

**Protected (Dashboard via Cloudflare Access):**
- `/dashboard` → Dashboard UI

**API:**
- `/api/health` → Health check
- `/api/todos` → Todo CRUD
- `/api/groceries` → Grocery CRUD
- `/api/gmail/*` → Gmail sync

## Cloudflare Integration

### Option 1: Cloudflare Tunnel (Recommended)

```bash
# Install on Pi
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
sudo dpkg -i cloudflared-linux-arm64.deb

# Authenticate and create tunnel
cloudflared tunnel login
cloudflared tunnel create daily-discover
cloudflared tunnel route dns daily-discover yourdomain.com

# Configure
cat > ~/.cloudflared/config.yml << EOF
tunnel: <TUNNEL-ID>
credentials-file: /home/gremlin/.cloudflared/<TUNNEL-ID>.json

ingress:
  - hostname: yourdomain.com
    service: http://localhost:8080
  - service: http_status:404
EOF

# Run as service
sudo cloudflared service install
sudo systemctl start cloudflared
```

### Option 2: Traditional DNS + Cloudflare Proxy

1. Point DNS to your public IP
2. Enable Cloudflare proxy (orange cloud)
3. Set up Page Rules for caching

## Pelican Blog

### Writing Posts

Create markdown files in `posts/`:

```markdown
Title: My Post
Date: 2026-02-26
Tags: python, flask
Summary: A brief summary

Your content here...
```

### Build Blog

```bash
pelican posts/ -o static/blog -s pelicanconf.py
```

### Customize Theme

Edit files in `themes/custom/`:
- `templates/*.html` - HTML structure
- `static/css/style.css` - Styling

## Troubleshooting

### Flask won't start
```bash
sudo journalctl -u daily-discover-flask -f
sudo systemctl restart daily-discover-flask
```

### Database connection issues
```bash
sudo systemctl status postgresql
psql -U matt -d daily_discover -c "SELECT 1;"
```

### Port already in use
```bash
lsof -i :8080
kill -9 <PID>
```

## Performance Tips for Pi

- Use 2-4 Gunicorn workers max on Pi 4
- Enable Cloudflare caching for static assets
- Keep PostgreSQL indexes on frequently queried columns
- Set up log rotation for `/var/log/daily-discover/`

---

© 2026 Daily Discover. Powered by Flask + Pelican.
