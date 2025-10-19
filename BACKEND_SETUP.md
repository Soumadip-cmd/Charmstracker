# Complete Backend Setup Commands

## Run these commands on your Hostinger server:

### 1. Upload the service file from Windows
```powershell
# Run this from Windows PowerShell:
scp D:\Charmstracker\charmstracker-api.service root@31.220.50.205:/root/Charmstracker/
```

---

## On Hostinger Server - Run these commands:

### 2. Setup Python Virtual Environment (if not done)
```bash
cd /root/Charmstracker/backend

# Check if venv exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
fi
```

### 3. Create .env file for backend
```bash
nano /root/Charmstracker/backend/.env
```

**Paste this content:**
```env
MONGO_URL=mongodb://localhost:27017/
DB_NAME=charmstracker
CORS_ORIGINS=http://charmstracker.com,http://www.charmstracker.com,https://charmstracker.com,https://www.charmstracker.com,http://31.220.50.205
```

**Save:** `Ctrl+X`, then `Y`, then `Enter`

---

### 4. Install and Setup MongoDB (if not installed)
```bash
# Check if MongoDB is installed
systemctl status mongod

# If not installed, run these:
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list

apt update
apt install -y mongodb-org

# Start MongoDB
systemctl start mongod
systemctl enable mongod
systemctl status mongod
```

---

### 5. Create and Start the Backend Service
```bash
# Copy service file to systemd
cp /root/Charmstracker/charmstracker-api.service /etc/systemd/system/

# Reload systemd to recognize new service
systemctl daemon-reload

# Enable service to start on boot
systemctl enable charmstracker-api

# Start the service
systemctl start charmstracker-api

# Check status
systemctl status charmstracker-api
```

---

### 6. Verify Backend is Running
```bash
# Check if service is active
systemctl status charmstracker-api

# Test API locally
curl http://127.0.0.1:8000/api/

# Check logs
journalctl -u charmstracker-api -f
```

---

### 7. Seed Database (Optional but Recommended)
```bash
cd /root/Charmstracker/backend
source venv/bin/activate
python seed_data.py
deactivate
```

---

### 8. Final Nginx Reload
```bash
# Reload nginx to apply all changes
systemctl reload nginx

# Check nginx status
systemctl status nginx
```

---

## Verify Everything is Working

```bash
# 1. Check backend service
systemctl status charmstracker-api

# 2. Check nginx
systemctl status nginx

# 3. Check MongoDB
systemctl status mongod

# 4. Test API
curl http://127.0.0.1:8000/api/
curl http://31.220.50.205/api/

# 5. View logs
journalctl -u charmstracker-api -n 50 --no-pager
tail -f /var/log/nginx/charmstracker_api_access.log
tail -f /var/log/nginx/charmstracker_frontend_access.log
```

---

## If Backend Service Fails, Check These:

### Check Python Virtual Environment
```bash
cd /root/Charmstracker/backend
ls -la venv/

# If venv doesn't exist, create it:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

### Check Backend Dependencies
```bash
cd /root/Charmstracker/backend
source venv/bin/activate
pip list
# Should see: fastapi, uvicorn, motor, python-dotenv, etc.
deactivate
```

### Check .env File
```bash
cat /root/Charmstracker/backend/.env
# Should show MONGO_URL and CORS_ORIGINS
```

### View Detailed Error Logs
```bash
journalctl -u charmstracker-api -n 100 --no-pager
```

### Test Backend Manually
```bash
cd /root/Charmstracker
source backend/venv/bin/activate
uvicorn backend.server:app --host 127.0.0.1 --port 8000
# Press Ctrl+C to stop
```

---

## Access Your Application

After all services are running:

- **Frontend:** http://charmstracker.com (or https:// after SSL)
- **API:** http://31.220.50.205/api/
- **API Health:** http://31.220.50.205/api/

---

## Quick Service Management Commands

```bash
# Start backend
systemctl start charmstracker-api

# Stop backend
systemctl stop charmstracker-api

# Restart backend
systemctl restart charmstracker-api

# View backend logs (live)
journalctl -u charmstracker-api -f

# View backend logs (last 50 lines)
journalctl -u charmstracker-api -n 50 --no-pager

# Check backend status
systemctl status charmstracker-api
```

---

## Complete Summary

1. ✅ Frontend built successfully
2. ✅ Nginx configured and tested
3. ⏳ Create backend systemd service (run commands above)
4. ⏳ Start backend service
5. ⏳ Verify everything works
6. ⏳ Setup DNS (point charmstracker.com to 31.220.50.205)
7. ⏳ Setup SSL with certbot (after DNS works)

Run the commands above on your Hostinger server to complete the setup! 🚀
