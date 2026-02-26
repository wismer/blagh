# Daily Discover - Separated Architecture

## Architecture

**Blog (Static):** Pelican → Cloudflare Pages  
**Dashboard/API (Dynamic):** Flask → Raspberry Pi

```
yourdomain.com          → Cloudflare Pages (blog)
  └─ Pelican static site
  
dashboard.yourdomain.com → Raspberry Pi (Flask)
  └─ /dashboard         → Protected dashboard UI
  └─ /api/*             → APIs (todos, groceries, gmail)
```

## Benefits

- **Performance**: Blog on CDN, instant worldwide
- **Reliability**: Blog stays up even if Pi goes down  
- **Resource efficiency**: Pi only handles dynamic requests
- **Scalability**: Static content auto-scales
- **Cost**: Cloudflare Pages is free

---

## Part 1: Deploy Blog to Cloudflare Pages

### Setup

1. **Create Cloudflare Pages project**
   - Go to Cloudflare Dashboard → Pages
   - Connect your GitHub repo
   - Configure build:
     - **Build command**: `pelican posts/ -o output -s publishconf.py`
     - **Build output**: `output`
     - **Root directory**: `/`

2. **Update domain in publishconf.py**
```python
SITEURL = 'https://yourdomain.com'
```

3. **Push to trigger deployment**
```bash
git add .
git commit -m "Deploy blog to Cloudflare Pages"
git push
```

### Local Blog Development

```bash
# Build blog locally
pelican posts/ -o output -s pelicanconf.py

# Preview with Pelican's dev server
pelican --listen -r

# Visit http://localhost:8000
```

### Writing Posts

Create markdown in `posts/`:

```markdown
Title: My Post Title
Date: 2026-02-26 10:00
Tags: python, flask
Summary: Brief description

Your content here...
```

---

## Part 2: Deploy Flask to Raspberry Pi

Flask now only serves **dashboard + APIs**. No blog routes.

### Setup on Pi

1. **Clone repo**
```bash
cd /home/gremlin
git clone <repo> blagh
cd blagh
```

2. **Install dependencies**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-prod.txt
```

3. **Configure environment**
```bash
cp .env.example .env
nano .env
# Set DATABASE_URL, GMAIL credentials, etc.
```

4. **Setup systemd service**
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

---

## Part 3: Cloudflare Tunnel Setup

Connect your Pi to Cloudflare securely (no port forwarding needed).

### Install Cloudflared on Pi

```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
sudo dpkg -i cloudflared-linux-arm64.deb
```

### Authenticate & Create Tunnel

```bash
cloudflared tunnel login
cloudflared tunnel create daily-discover
cloudflared tunnel route dns daily-discover dashboard.yourdomain.com
```

### Configure Tunnel

Create `~/.cloudflared/config.yml`:

```yaml
tunnel: <TUNNEL-ID>
credentials-file: /home/gremlin/.cloudflared/<TUNNEL-ID>.json

ingress:
  - hostname: dashboard.yourdomain.com
    service: http://localhost:8080
  - service: http_status:404
```

### Run as Service

```bash
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

---

## DNS Configuration

In Cloudflare DNS:

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| CNAME | yourdomain.com | (Cloudflare Pages URL) | ✅ Proxied |
| CNAME | dashboard | (Tunnel CNAME) | ✅ Proxied |

---

## Security

### Protect Dashboard with Cloudflare Access

1. Go to **Cloudflare Zero Trust** → Access → Applications
2. Create new application:
   - **Domain**: `dashboard.yourdomain.com`
   - **Path**: `/dashboard`
   - **Policy**: Require your email or Google Workspace

Now only authorized users can access the dashboard!

---

## Local Development

### Blog (Pelican)
```bash
pelican --listen -r
# Visit http://localhost:8000
```

### Dashboard/API (Flask)
```bash
python run.py
# Visit http://localhost:8080/dashboard
```

---

## Deployment Workflow

### Blog Updates
```bash
# Edit markdown in posts/
git add posts/
git commit -m "New blog post"
git push
# Cloudflare Pages auto-deploys
```

### Dashboard/API Updates
```bash
git push
# SSH into Pi
ssh gremlin@yourpi
cd blagh
./deploy-hybrid.sh
```

---

## Troubleshooting

### Blog not updating on Cloudflare
- Check Cloudflare Pages build logs
- Verify `publishconf.py` has correct SITEURL

### Dashboard not accessible
```bash
# On Pi
sudo systemctl status daily-discover-flask
sudo journalctl -u daily-discover-flask -f
```

### Tunnel not working
```bash
# On Pi
sudo systemctl status cloudflared
sudo journalctl -u cloudflared -f
```

---

## Cost

- **Cloudflare Pages**: Free (500 builds/month)
- **Cloudflare Tunnel**: Free
- **Cloudflare Access**: Free (up to 50 users)
- **Total**: $0/month 🎉

---

## Architecture Benefits

✅ Blog on global CDN (fast worldwide)  
✅ Flask only handles dynamic requests  
✅ Pi failure doesn't affect blog  
✅ Free hosting for static content  
✅ Easy to scale  
✅ Cloudflare DDoS protection  
✅ Automatic HTTPS  

---

© 2026 Daily Discover
