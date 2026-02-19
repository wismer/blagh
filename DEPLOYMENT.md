# Daily Discover - Production Deployment Guide

## Prerequisites

### Domain Setup
1. **DNS Configuration**
   - Point `gremlin.computer` A record to your Raspberry Pi's public IP
   - Or use dynamic DNS if you have a dynamic IP
   - Wait for DNS propagation (can take up to 24-48 hours)

### Raspberry Pi Requirements
- Raspberry Pi 3 or newer (4 recommended)
- Raspberry Pi OS (64-bit recommended)
- At least 2GB RAM
- 16GB+ SD card
- Stable internet connection
- SSH access enabled

### Port Forwarding (if behind router)
- Forward port 80 (HTTP) to your Pi
- Forward port 443 (HTTPS) to your Pi

## Deployment Steps

### 1. Prepare Your Code

On your development machine:
```bash
# Update production redirect URI in .env.production
# Push code to Git repository (GitHub, GitLab, etc.)
git add .
git commit -m "Ready for production deployment"
git push origin main
```

### 2. Access Your Raspberry Pi

```bash
ssh pi@YOUR_PI_IP
```

### 3. Update System

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 4. Clone Repository

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/daily-discover.git
cd daily-discover
```

### 5. Run Deployment Script

```bash
# Make script executable
chmod +x deploy.sh

# Edit the script to add your email for Let's Encrypt
nano deploy.sh
# Change: YOUR_EMAIL@example.com to your actual email

# Run deployment (requires sudo)
sudo ./deploy.sh
```

The script will:
- Install all dependencies (Python, PostgreSQL, Nginx)
- Create and configure the database
- Set up Python virtual environment
- Generate secure credentials
- Configure Nginx reverse proxy
- Set up SSL with Let's Encrypt
- Create systemd service for auto-start
- Start the application

### 6. Verify Deployment

```bash
# Check application status
sudo systemctl status daily-discover

# View application logs
journalctl -u daily-discover -f

# Check Nginx status
sudo systemctl status nginx

# Test the site
curl https://gremlin.computer/api/health
```

## Manual Configuration Steps

### Update Google OAuth Redirect URI

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to "APIs & Services" > "Credentials"
4. Edit your OAuth 2.0 Client ID
5. Add authorized redirect URI: `https://gremlin.computer/oauth2callback`
6. Save changes

### Create Initial User (Optional)

```bash
sudo -u postgres psql -d daily_discover <<EOF
INSERT INTO users (id, username, email, password_hash) 
VALUES (
  gen_random_uuid(), 
  'admin', 
  'your-email@example.com', 
  'temporary-hash'
);
EOF
```

## iOS Shortcuts Configuration

### Grocery List Shortcut

1. Open Shortcuts app on iOS
2. Create new shortcut
3. Add actions:
   - **Ask for Input**: "What do you want to add?"
   - **Text**: Store input in variable "items"
   - **Get Contents of URL**: `https://gremlin.computer/api/voice-input`
     - Method: POST
     - Headers: `Content-Type: application/json`
     - Body: 
       ```json
       {
         "type": "groceries",
         "items": ["{{items}}"]
       }
       ```
4. Name it "Add Groceries"
5. Add to Siri: "Hey Siri, add groceries"

### TODO Shortcut

Similar setup but use:
```json
{
  "type": "todo",
  "text": "{{input}}",
  "priority": 0
}
```

## Service Management

### Start/Stop/Restart

```bash
# Start service
sudo systemctl start daily-discover

# Stop service
sudo systemctl stop daily-discover

# Restart service
sudo systemctl restart daily-discover

# View status
sudo systemctl status daily-discover

# Enable auto-start on boot
sudo systemctl enable daily-discover
```

### View Logs

```bash
# Application logs
journalctl -u daily-discover -f

# Nginx access logs
tail -f /var/log/nginx/daily-discover-access.log

# Nginx error logs
tail -f /var/log/nginx/daily-discover-error.log
```

### Update Application

```bash
cd /home/pi/daily-discover
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart daily-discover
```

## Security Considerations

### Firewall Setup (Optional but Recommended)

```bash
sudo apt-get install ufw
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Regular Updates

```bash
# Set up automatic security updates
sudo apt-get install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### SSL Certificate Renewal

Certbot auto-renews certificates. Check status:
```bash
sudo certbot renew --dry-run
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs for errors
journalctl -u daily-discover -n 50

# Check if port is in use
sudo netstat -tlnp | grep 5000

# Verify database connection
sudo -u pi psql -h localhost -d daily_discover -U daily_discover_user
```

### Nginx Issues

```bash
# Test configuration
sudo nginx -t

# Reload configuration
sudo nginx -s reload

# Check error logs
tail -f /var/log/nginx/error.log
```

### Database Issues

```bash
# Connect to database
sudo -u postgres psql -d daily_discover

# Check tables
\dt

# Check user permissions
\du
```

### SSL Certificate Issues

```bash
# Check certificate status
sudo certbot certificates

# Manual renewal
sudo certbot renew

# Check Nginx SSL configuration
sudo nginx -t
```

## Performance Tuning

### Increase Workers (for Pi 4)

Edit `/etc/systemd/system/daily-discover.service`:
```
ExecStart=/home/pi/daily-discover/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 4 --timeout 120 app:app
```

Then reload:
```bash
sudo systemctl daemon-reload
sudo systemctl restart daily-discover
```

### PostgreSQL Tuning

Edit `/etc/postgresql/*/main/postgresql.conf`:
```
shared_buffers = 128MB
effective_cache_size = 512MB
maintenance_work_mem = 64MB
```

Restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

## Backup Strategy

### Database Backup

```bash
# Create backup script
cat > ~/backup-daily-discover.sh <<'EOF'
#!/bin/bash
BACKUP_DIR="/home/pi/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
pg_dump -U daily_discover_user -h localhost daily_discover | gzip > $BACKUP_DIR/daily-discover-$DATE.sql.gz
# Keep only last 7 days
find $BACKUP_DIR -name "daily-discover-*.sql.gz" -mtime +7 -delete
EOF

chmod +x ~/backup-daily-discover.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /home/pi/backup-daily-discover.sh") | crontab -
```

### Restore from Backup

```bash
gunzip -c /home/pi/backups/daily-discover-YYYYMMDD_HHMMSS.sql.gz | \
  psql -U daily_discover_user -h localhost -d daily_discover
```

## Monitoring

### Set up Basic Monitoring

```bash
# Install monitoring tools
sudo apt-get install htop iotop

# Check system resources
htop

# Monitor disk I/O
sudo iotop
```

### Log Rotation

Nginx logs are rotated automatically. For application logs:

```bash
# Limit journald logs to 100MB
sudo journalctl --vacuum-size=100M
```

## Support

- Application logs: `journalctl -u daily-discover -f`
- Check service status: `systemctl status daily-discover`
- Database issues: Check PostgreSQL logs in `/var/log/postgresql/`
- Nginx issues: Check `/var/log/nginx/daily-discover-error.log`
