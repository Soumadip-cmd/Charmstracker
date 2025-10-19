# Fix Mixed Content Error (HTTPS/HTTP)

## The Problem:
Your site is on HTTPS (https://charmstracker.com) but trying to call HTTP API.
Browsers block HTTP requests from HTTPS pages for security.

## ✅ Solution: Use API on Same Domain

Instead of calling `http://31.220.50.205/api/`, call `https://charmstracker.com/api/`

---

## 🚀 Quick Fix Commands:

### Step 1: Update Files on Windows
Already done! Now push to GitHub:

```powershell
cd D:\Charmstracker
git add .
git commit -m "Fix mixed content - use HTTPS API"
git push origin main
```

### Step 2: On Hostinger Server

```bash
# Pull latest code
cd /root/Charmstracker
git pull origin main

# Update nginx API config to listen on main domain
cp /root/Charmstracker/nginx_api.conf /etc/nginx/sites-available/charmstracker-api

# Test nginx
nginx -t

# Restart nginx
systemctl restart nginx

# Rebuild frontend with new API URL
cd frontend
rm -rf build
yarn build

# Restart services
systemctl restart nginx

# Test API on domain
curl https://charmstracker.com/api/
curl https://charmstracker.com/api/charms
```

---

## 📋 All-in-One Command (Server):

```bash
cd /root/Charmstracker && \
git pull origin main && \
cp nginx_api.conf /etc/nginx/sites-available/charmstracker-api && \
nginx -t && \
systemctl restart nginx && \
cd frontend && \
rm -rf build && \
yarn build && \
systemctl restart nginx && \
echo "✅ Testing API..." && \
sleep 2 && \
curl https://charmstracker.com/api/charms
```

---

## ✅ What This Does:

1. Changes API URL from `http://31.220.50.205` to `https://charmstracker.com`
2. Nginx will handle both frontend AND API on same domain
3. SSL certificate covers both
4. No more mixed content errors!

---

## 🧪 Test After Deploy:

```bash
# Should work now
curl https://charmstracker.com/api/
curl https://charmstracker.com/api/charms

# Check in browser
# Open: https://charmstracker.com
# Check browser console - no more mixed content errors!
```

---

## 🔍 Verify API Endpoint:

Your API will be available at:
- ✅ `https://charmstracker.com/api/`
- ✅ `https://charmstracker.com/api/charms`
- ✅ `https://charmstracker.com/api/trending`
- ✅ `https://charmstracker.com/api/market-overview`

All on HTTPS! 🔒
