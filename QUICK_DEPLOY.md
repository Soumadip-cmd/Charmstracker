# Quick Deployment Commands

## Upload nginx configs to server

**Run from Windows PowerShell:**
```powershell
scp D:\Charmstracker\nginx_api.conf root@31.220.50.205:/root/Charmstracker/
scp D:\Charmstracker\nginx_frontend.conf root@31.220.50.205:/root/Charmstracker/
```

---

## On Hostinger Server - Complete Setup

### 1. Update Backend CORS
```bash
nano /root/Charmstracker/backend/.env
```

**Add this:**
```env
MONGO_URL=mongodb://localhost:27017/
DB_NAME=charmstracker
CORS_ORIGINS=http://charmstracker.com,http://www.charmstracker.com,https://charmstracker.com,https://www.charmstracker.com,http://31.220.50.205
```

Save: `Ctrl+X`, `Y`, `Enter`

### 2. Create Frontend .env.production
```bash
nano /root/Charmstracker/frontend/.env.production
```

**Add this:**
```env
REACT_APP_BACKEND_URL=http://31.220.50.205
```

Save: `Ctrl+X`, `Y`, `Enter`

### 3. Rebuild Frontend
```bash
cd /root/Charmstracker/frontend
yarn build
```

### 4. Update Nginx Configs
```bash
cp /root/Charmstracker/nginx_api.conf /etc/nginx/sites-available/charmstracker-api
cp /root/Charmstracker/nginx_frontend.conf /etc/nginx/sites-available/charmstracker-frontend

# Test nginx
nginx -t

# Reload nginx
systemctl reload nginx
```

### 5. Restart Backend
```bash
systemctl restart charmstracker-api
systemctl status charmstracker-api
```

---

## Setup DNS (Do this first!)

Go to your domain registrar and add these DNS records:

### A Records:
```
Type: A
Name: @
Value: 31.220.50.205

Type: A  
Name: www
Value: 31.220.50.205
```

**Wait 1-2 hours for DNS to propagate**

Check DNS: https://dnschecker.org/

---

## Setup SSL (After DNS works)

```bash
# Install certbot
apt update
apt install -y certbot python3-certbot-nginx

# Get SSL certificate
certbot --nginx -d charmstracker.com -d www.charmstracker.com

# Follow prompts and choose to redirect HTTP to HTTPS
```

---

## After SSL is Setup

Update backend CORS to include HTTPS:
```bash
nano /root/Charmstracker/backend/.env
```

**Update to:**
```env
CORS_ORIGINS=http://charmstracker.com,http://www.charmstracker.com,https://charmstracker.com,https://www.charmstracker.com,http://31.220.50.205
```

Restart backend:
```bash
systemctl restart charmstracker-api
```

---

## Verify Everything

```bash
# Check services
systemctl status charmstracker-api
systemctl status nginx

# Test API
curl http://31.220.50.205/api/

# View logs
journalctl -u charmstracker-api -f
tail -f /var/log/nginx/charmstracker_frontend_access.log
tail -f /var/log/nginx/charmstracker_api_access.log
```

---

## Access URLs

- **Frontend:** http://charmstracker.com (or https:// after SSL)
- **Frontend (www):** http://www.charmstracker.com
- **API:** http://31.220.50.205/api/

---

## Complete Sequence

1. ✅ Setup DNS records → Wait 1-2 hours
2. ✅ Upload nginx configs from Windows
3. ✅ Update backend .env with CORS
4. ✅ Create frontend .env.production
5. ✅ Rebuild frontend
6. ✅ Copy nginx configs to sites-available
7. ✅ Test and reload nginx
8. ✅ Restart backend service
9. ✅ Setup SSL with certbot (after DNS)
10. ✅ Update CORS to include HTTPS
11. ✅ Test in browser

Done! 🚀
