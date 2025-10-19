# Fix Conflicting Server Names

## The Problem:
Both nginx-api and nginx-frontend are listening on charmstracker.com
This creates a conflict and breaks SSL.

## ✅ Solution:
Disable the API config since frontend now handles API proxying.

---

## 🚀 Run These Commands on Server:

```bash
# 1. Disable the API nginx config (we don't need it anymore)
rm /etc/nginx/sites-enabled/charmstracker-api

# 2. Keep only the frontend config (it handles both frontend and API)
ls /etc/nginx/sites-enabled/

# 3. Test nginx
nginx -t

# 4. Restart nginx
systemctl restart nginx

# 5. Check if SSL is working
curl https://charmstracker.com

# 6. Test API
curl https://charmstracker.com/api/charms

# 7. Check services
systemctl status nginx --no-pager
systemctl status charmstracker-api --no-pager
```

---

## 📋 All-in-One Command:

```bash
rm /etc/nginx/sites-enabled/charmstracker-api && \
nginx -t && \
systemctl restart nginx && \
sleep 2 && \
echo "✅ Testing frontend..." && \
curl -I https://charmstracker.com && \
echo "" && \
echo "✅ Testing API..." && \
curl https://charmstracker.com/api/charms
```

---

## 🔍 What This Does:

**Before:**
- `charmstracker-api` config: Listens on charmstracker.com ❌
- `charmstracker-frontend` config: Listens on charmstracker.com ❌
- **Result:** Conflict! SSL breaks

**After:**
- `charmstracker-api` config: **DISABLED** ✅
- `charmstracker-frontend` config: Handles both frontend + API ✅
- **Result:** No conflict! Everything works

---

## ✅ Expected Result:

```bash
# Should show 200 OK
curl -I https://charmstracker.com

# Should show JSON data
curl https://charmstracker.com/api/charms
```

Then open **https://charmstracker.com** in browser - it will work! 🎉

---

## 🏗️ Architecture After Fix:

```
Browser → https://charmstracker.com → Nginx Frontend Config
                                           ↓
                      /             or     /api
                      ↓                     ↓
                 Static Files      → Backend (127.0.0.1:8000)
```

Only ONE nginx config handling everything!
