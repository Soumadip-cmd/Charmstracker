# Fix 502 Bad Gateway - API Not Connecting

## ✅ Progress So Far:
- ✅ Frontend SSL working (https://charmstracker.com returns 200)
- ✅ API SSL configured (https://charms.freelixe.com)
- ❌ API returning 502 Bad Gateway (backend not accessible)

---

## 🔍 Diagnose the Issue:

```bash
# Check if backend is running
systemctl status charmstracker-api --no-pager

# Check if backend is listening on port 8000
netstat -tlnp | grep 8000
# OR
ss -tlnp | grep 8000

# Check backend logs
journalctl -u charmstracker-api -n 50 --no-pager

# Check nginx error logs
tail -50 /var/log/nginx/charmstracker_api_error.log
```

---

## 🔧 Fix Backend Service:

Most likely issue: Backend service not running or crashed.

```bash
# Restart backend service
systemctl restart charmstracker-api

# Check status
systemctl status charmstracker-api --no-pager

# If not running, check why
journalctl -u charmstracker-api -n 50 --no-pager

# Test backend directly
curl http://127.0.0.1:8000/api/
curl http://127.0.0.1:8000/api/charms
```

---

## 📋 All-in-One Fix Command:

```bash
# Update backend .env
cat > /root/Charmstracker/backend/.env << 'EOF'
MONGO_URL="mongodb+srv://carefreelixe_db_user:d9po0rKPJwchyCBE@laundry.bhx3jw0.mongodb.net/?retryWrites=true&w=majority"
DB_NAME="charmtracker_production"
CORS_ORIGINS="https://charmstracker.com,https://www.charmstracker.com,https://charms.freelixe.com,http://localhost:3000"
EOF

# Restart backend
systemctl restart charmstracker-api

# Wait for it to start
sleep 3

# Check status
systemctl status charmstracker-api --no-pager

# Test local backend
echo "Testing local backend..."
curl http://127.0.0.1:8000/api/

# Test through nginx
echo "Testing through nginx..."
curl https://charms.freelixe.com/api/
curl https://charms.freelixe.com/api/charms

# Test frontend
echo "Testing frontend..."
curl -I https://charmstracker.com
```

---

## 🚀 Complete Fix (Copy This):

```bash
cd /root/Charmstracker && \
cat > backend/.env << 'EOF'
MONGO_URL="mongodb+srv://carefreelixe_db_user:d9po0rKPJwchyCBE@laundry.bhx3jw0.mongodb.net/?retryWrites=true&w=majority"
DB_NAME="charmtracker_production"
CORS_ORIGINS="https://charmstracker.com,https://www.charmstracker.com,https://charms.freelixe.com,http://localhost:3000"
EOF

systemctl restart charmstracker-api && \
sleep 3 && \
echo "✅ Checking backend status..." && \
systemctl status charmstracker-api --no-pager && \
echo "" && \
echo "✅ Testing local backend..." && \
curl http://127.0.0.1:8000/api/ && \
echo "" && \
echo "✅ Testing API subdomain..." && \
curl https://charms.freelixe.com/api/ && \
echo "" && \
echo "✅ Getting charms data..." && \
curl https://charms.freelixe.com/api/charms
```

---

## 🔍 If Backend Won't Start:

```bash
# Check what's wrong
journalctl -u charmstracker-api -n 100 --no-pager

# Common issues:
# 1. Port 8000 already in use
# 2. Python environment issue
# 3. Import errors
# 4. Database connection issue

# Kill any process on port 8000
lsof -ti:8000 | xargs kill -9

# Try starting manually to see errors
cd /root/Charmstracker
/usr/bin/python3.12 -m uvicorn backend.server:app --host 127.0.0.1 --port 8000
```

---

## 🧪 Verification:

After the fix, you should see:

```bash
# Backend status: Active (running)
systemctl status charmstracker-api

# Local backend works
curl http://127.0.0.1:8000/api/
# Returns: {"message":"CharmTracker API is running"}

# API subdomain works
curl https://charms.freelixe.com/api/charms
# Returns: JSON array of charms

# Frontend works
curl https://charmstracker.com
# Returns: HTML with React app
```

---

## 📝 Summary:

The 502 Bad Gateway means nginx can't reach your backend on 127.0.0.1:8000. 

Most likely causes:
1. Backend service crashed or not running
2. Backend listening on wrong port/interface
3. Backend startup error (check logs)

Run the "Complete Fix" command above to restart the backend and test everything! 🚀
