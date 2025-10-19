# Fix API 301 Redirect Issue

## The Problem:
Frontend nginx is proxying to `http://31.220.50.205/api` which redirects.
Should proxy directly to local backend at `127.0.0.1:8000`.

## ✅ Solution Applied:

Changed nginx frontend config to proxy API requests to local backend.

---

## 🚀 Deploy Fix:

### Step 1: Push to GitHub (Windows):
```powershell
cd D:\Charmstracker
git add .
git commit -m "Fix API proxy to use local backend"
git push origin main
```

### Step 2: Apply on Server:
```bash
# Pull latest
cd /root/Charmstracker
git pull origin main

# Update nginx frontend config
cp nginx_frontend.conf /etc/nginx/sites-available/charmstracker-frontend

# Test nginx
nginx -t

# Restart nginx
systemctl restart nginx

# Test API
curl https://charmstracker.com/api/charms
```

---

## 📋 All-in-One Command (Server):

```bash
cd /root/Charmstracker && \
git pull origin main && \
cp nginx_frontend.conf /etc/nginx/sites-available/charmstracker-frontend && \
nginx -t && \
systemctl restart nginx && \
echo "✅ Testing API..." && \
curl https://charmstracker.com/api/charms
```

---

## ✅ Expected Result:

You should see JSON data with charms, not HTML redirect!

```json
{
  "charms": [...],
  "total": 20,
  "page": 1
}
```

---

## 🧪 Additional Tests:

```bash
# Test different endpoints
curl https://charmstracker.com/api/
curl https://charmstracker.com/api/trending
curl https://charmstracker.com/api/market-overview

# Check backend is running
systemctl status charmstracker-api --no-pager

# View logs if needed
journalctl -u charmstracker-api -n 20 --no-pager
```

After this, open **https://charmstracker.com** in browser - data should load! 🎉
