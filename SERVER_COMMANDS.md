# COPY AND PASTE THESE COMMANDS ON HOSTINGER SERVER

## All commands in one block - copy and paste this entire block:

```bash
# Navigate to project directory
cd /root/Charmstracker/backend

# Create virtual environment if needed
if [ ! -d "venv" ]; then python3 -m venv venv; fi

# Install dependencies
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Create .env file
cat > /root/Charmstracker/backend/.env << 'EOF'
MONGO_URL=mongodb://localhost:27017/
DB_NAME=charmstracker
CORS_ORIGINS=http://charmstracker.com,http://www.charmstracker.com,https://charmstracker.com,https://www.charmstracker.com,http://31.220.50.205
EOF

# Install systemd service
cp /root/Charmstracker/charmstracker-api.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable charmstracker-api
systemctl start charmstracker-api

# Check status
systemctl status charmstracker-api

# Test API
sleep 3
curl http://127.0.0.1:8000/api/

# Reload nginx
systemctl reload nginx

echo "Done! Check status above."
```

---

## Or run step by step:

### 1. Setup Virtual Environment
```bash
cd /root/Charmstracker/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

### 2. Create .env file
```bash
cat > /root/Charmstracker/backend/.env << 'EOF'
MONGO_URL=mongodb://localhost:27017/
DB_NAME=charmstracker
CORS_ORIGINS=http://charmstracker.com,http://www.charmstracker.com,https://charmstracker.com,https://www.charmstracker.com,http://31.220.50.205
EOF
```

### 3. Install and start service
```bash
cp /root/Charmstracker/charmstracker-api.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable charmstracker-api
systemctl start charmstracker-api
systemctl status charmstracker-api
```

### 4. Test and reload
```bash
curl http://127.0.0.1:8000/api/
systemctl reload nginx
```

---

## Verify Everything

```bash
# Check all services
systemctl status charmstracker-api
systemctl status nginx
systemctl status mongod

# View logs
journalctl -u charmstracker-api -f

# Test API
curl http://127.0.0.1:8000/api/
curl http://31.220.50.205/api/
```

---

## If MongoDB is not installed:

```bash
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list

apt update
apt install -y mongodb-org
systemctl start mongod
systemctl enable mongod
```

---

## Seed Database (Optional)

```bash
cd /root/Charmstracker/backend
source venv/bin/activate
python seed_data.py
deactivate
```

---

## Access Your App

- Frontend: http://charmstracker.com
- API: http://31.220.50.205/api/

Done! 🚀
