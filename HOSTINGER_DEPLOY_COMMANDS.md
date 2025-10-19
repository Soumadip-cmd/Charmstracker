# CharmTracker Deployment Commands for Hostinger
## Your Server Structure: /root/Charmstracker

---

## Current Status Check

```bash
# You are here: /root/Charmstracker/frontend
# Building with: yarn build

# Check your current location
pwd
# Should show: /root/Charmstracker/frontend
```

---

## Step 1: Complete Frontend Build

```bash
# You're already running this:
cd /root/Charmstracker/frontend
yarn build

# Wait for build to complete...
# This creates: /root/Charmstracker/frontend/build/
```

---

## Step 2: Setup Backend Python Virtual Environment

```bash
# Navigate to backend
cd /root/Charmstracker/backend

# Create virtual environment (if not already created)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env
```

**Add this to .env file:**
```env
MONGO_URL=mongodb://localhost:27017/
DB_NAME=charmstracker
CORS_ORIGINS=http://31.220.50.205,http://www.31.220.50.205
```

**Save and exit:** Press `Ctrl+X`, then `Y`, then `Enter`

---

## Step 3: Create Backend Systemd Service

```bash
# Create service file
nano /etc/systemd/system/charmstracker-api.service
```

**Paste this content:**
```ini
[Unit]
Description=CharmTracker FastAPI Application
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/root/Charmstracker
Environment="PATH=/root/Charmstracker/backend/venv/bin"
ExecStart=/root/Charmstracker/backend/venv/bin/uvicorn backend.server:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Save and exit:** Press `Ctrl+X`, then `Y`, then `Enter`

```bash
# Reload systemd
systemctl daemon-reload

# Enable service to start on boot
systemctl enable charmstracker-api

# Start the service
systemctl start charmstracker-api

# Check status
systemctl status charmstracker-api
```

---

## Step 4: Upload Nginx Configurations

**On your LOCAL Windows machine (PowerShell):**

```powershell
# Upload nginx configs to server
scp D:\Charmstracker\nginx_api.conf root@31.220.50.205:/root/Charmstracker/
scp D:\Charmstracker\nginx_frontend.conf root@31.220.50.205:/root/Charmstracker/
```

---

## Step 5: Configure Nginx on Server

```bash
# Copy API nginx config
cp /root/Charmstracker/nginx_api.conf /etc/nginx/sites-available/charmstracker-api

# Copy Frontend nginx config
cp /root/Charmstracker/nginx_frontend.conf /etc/nginx/sites-available/charmstracker-frontend

# Enable sites by creating symbolic links
ln -s /etc/nginx/sites-available/charmstracker-api /etc/nginx/sites-enabled/
ln -s /etc/nginx/sites-available/charmstracker-frontend /etc/nginx/sites-enabled/

# Remove default nginx site (optional)
rm /etc/nginx/sites-enabled/default

# Test nginx configuration
nginx -t

# If test passes, reload nginx
systemctl reload nginx
systemctl restart nginx
```

---

## Step 6: Setup MongoDB (if not already installed)

```bash
# Check if MongoDB is installed
systemctl status mongod

# If not installed:
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list

apt update
apt install -y mongodb-org

# Start and enable MongoDB
systemctl start mongod
systemctl enable mongod
systemctl status mongod
```

---

## Step 7: Seed Database (Optional)

```bash
# Navigate to backend
cd /root/Charmstracker/backend

# Activate virtual environment
source venv/bin/activate

# Run seed script
python seed_data.py

# Deactivate virtual environment
deactivate
```

---

## Step 8: Setup Firewall

```bash
# Allow SSH (IMPORTANT!)
ufw allow 22/tcp

# Allow HTTP
ufw allow 80/tcp

# Allow HTTPS (for future)
ufw allow 443/tcp

# Enable firewall
ufw --force enable

# Check status
ufw status
```

---

## Step 9: Verify Everything is Working

```bash
# Check backend service
systemctl status charmstracker-api

# Check nginx
systemctl status nginx

# Check MongoDB
systemctl status mongod

# Test API locally
curl http://127.0.0.1:8000/api/

# Test API via nginx
curl http://31.220.50.205/api/

# View backend logs
journalctl -u charmstracker-api -f

# View nginx logs
tail -f /var/log/nginx/charmstracker_api_access.log
tail -f /var/log/nginx/charmstracker_frontend_access.log
```

---

## Step 10: Access Your Application

- **API Endpoint:** http://31.220.50.205/api/
- **Frontend:** http://31.220.50.205 or http://www.31.220.50.205

---

## Quick Reference Commands

### Restart Backend
```bash
systemctl restart charmstracker-api
systemctl status charmstracker-api
journalctl -u charmstracker-api -f
```

### Restart Nginx
```bash
nginx -t
systemctl reload nginx
systemctl restart nginx
```

### View Logs
```bash
# Backend logs
journalctl -u charmstracker-api -n 50 --no-pager
journalctl -u charmstracker-api -f

# Nginx logs
tail -f /var/log/nginx/charmstracker_api_access.log
tail -f /var/log/nginx/charmstracker_api_error.log
tail -f /var/log/nginx/charmstracker_frontend_access.log
tail -f /var/log/nginx/charmstracker_frontend_error.log
```

### Update Application
```bash
# Pull latest code
cd /root/Charmstracker
git pull origin main

# Rebuild frontend
cd frontend
yarn install
yarn build

# Restart backend (if code changed)
systemctl restart charmstracker-api

# Reload nginx
systemctl reload nginx
```

### MongoDB Commands
```bash
# Access MongoDB shell
mongosh

# In MongoDB shell:
use charmstracker
db.charms.find().pretty()
exit

# Backup database
mongodump --db charmstracker --out /root/backups/mongodb/$(date +%Y%m%d)

# Restore database
mongorestore --db charmstracker /root/backups/mongodb/20241019/charmstracker/
```

---

## Troubleshooting

### Backend won't start
```bash
# Check logs
journalctl -u charmstracker-api -n 50 --no-pager

# Check if port 8000 is available
netstat -tlnp | grep 8000

# Kill process on port 8000 if needed
kill -9 $(lsof -t -i:8000)

# Restart service
systemctl restart charmstracker-api
```

### Nginx errors
```bash
# Test config
nginx -t

# Check error logs
tail -f /var/log/nginx/error.log

# Check if ports are available
netstat -tlnp | grep :80
```

### MongoDB connection issues
```bash
# Check MongoDB status
systemctl status mongod

# Restart MongoDB
systemctl restart mongod

# Check MongoDB logs
tail -f /var/log/mongodb/mongod.log
```

### Permission issues
```bash
# Fix permissions for application directory
chown -R root:root /root/Charmstracker
chmod -R 755 /root/Charmstracker

# Fix nginx permissions for build folder
chmod -R 755 /root/Charmstracker/frontend/build
```

---

## Complete Deployment Sequence (Run these in order)

```bash
# 1. Build frontend (YOU'RE HERE)
cd /root/Charmstracker/frontend
yarn build

# 2. Setup backend
cd /root/Charmstracker/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
nano .env  # Add MongoDB config
deactivate

# 3. Create systemd service
nano /etc/systemd/system/charmstracker-api.service  # Paste service config
systemctl daemon-reload
systemctl enable charmstracker-api
systemctl start charmstracker-api
systemctl status charmstracker-api

# 4. Configure Nginx
cp /root/Charmstracker/nginx_api.conf /etc/nginx/sites-available/charmstracker-api
cp /root/Charmstracker/nginx_frontend.conf /etc/nginx/sites-available/charmstracker-frontend
ln -s /etc/nginx/sites-available/charmstracker-api /etc/nginx/sites-enabled/
ln -s /etc/nginx/sites-available/charmstracker-frontend /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

# 5. Setup firewall
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# 6. Verify
systemctl status charmstracker-api
systemctl status nginx
curl http://127.0.0.1:8000/api/
curl http://31.220.50.205/api/

# 7. Access in browser
# http://31.220.50.205
```

---

## Important Notes

1. **Your directory:** `/root/Charmstracker` (not `/var/www/charmstracker`)
2. **User:** Running as `root` (not `www-data`)
3. **Frontend build:** `/root/Charmstracker/frontend/build`
4. **Backend path:** `/root/Charmstracker/backend`

All configs have been updated to match your actual directory structure! 🚀
