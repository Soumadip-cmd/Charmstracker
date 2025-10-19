# DNS Setup Guide for charmstracker.com

## Your Configuration:
- **Frontend (Website):** charmstracker.com & www.charmstracker.com
- **Backend (API):** 31.220.50.205

---

## Step 1: Configure DNS Records

Go to your domain registrar (where you bought charmstracker.com) and add these DNS records:

### A Records:
```
Type: A
Name: @
Value: 31.220.50.205
TTL: 3600 (or default)

Type: A
Name: www
Value: 31.220.50.205
TTL: 3600 (or default)
```

**Common Domain Registrars:**
- **Namecheap:** Advanced DNS → Add New Record
- **GoDaddy:** DNS Management → Add Record
- **Cloudflare:** DNS → Add Record
- **Google Domains:** DNS → Custom Records

### DNS Propagation:
- Changes can take 5 minutes to 48 hours to propagate
- Usually takes 1-2 hours
- Check status: https://dnschecker.org/

---

## Step 2: Update Backend CORS Settings

Update your backend `.env` file to allow requests from your domain:

**On Hostinger Server:**
```bash
nano /root/Charmstracker/backend/.env
```

**Update CORS_ORIGINS to:**
```env
MONGO_URL=mongodb://localhost:27017/
DB_NAME=charmstracker
CORS_ORIGINS=http://charmstracker.com,http://www.charmstracker.com,https://charmstracker.com,https://www.charmstracker.com,http://31.220.50.205
```

Save and restart backend:
```bash
systemctl restart charmstracker-api
```

---

## Step 3: Upload Updated Nginx Configs

**From your Windows machine (PowerShell):**
```powershell
scp D:\Charmstracker\nginx_api.conf root@31.220.50.205:/root/Charmstracker/
scp D:\Charmstracker\nginx_frontend.conf root@31.220.50.205:/root/Charmstracker/
```

**On Hostinger Server:**
```bash
# Backup old configs
cp /etc/nginx/sites-available/charmstracker-api /etc/nginx/sites-available/charmstracker-api.backup
cp /etc/nginx/sites-available/charmstracker-frontend /etc/nginx/sites-available/charmstracker-frontend.backup

# Copy new configs
cp /root/Charmstracker/nginx_api.conf /etc/nginx/sites-available/charmstracker-api
cp /root/Charmstracker/nginx_frontend.conf /etc/nginx/sites-available/charmstracker-frontend

# Test nginx config
nginx -t

# Reload nginx
systemctl reload nginx
```

---

## Step 4: Update Frontend API URL

Update your frontend to use the correct API URL:

**Edit:** `/root/Charmstracker/frontend/src/services/api.js`

```javascript
// Change API base URL to use IP address
const API_BASE_URL = 'http://31.220.50.205/api';

// Or use environment variable
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://31.220.50.205/api';
```

**Rebuild frontend:**
```bash
cd /root/Charmstracker/frontend
yarn build
systemctl reload nginx
```

---

## Step 5: Setup SSL Certificate (HTTPS)

Once DNS is working, secure your site with SSL:

**On Hostinger Server:**
```bash
# Install Certbot
apt update
apt install -y certbot python3-certbot-nginx

# Get SSL certificate for your domain
certbot --nginx -d charmstracker.com -d www.charmstracker.com

# Follow the prompts:
# - Enter your email
# - Agree to terms
# - Choose to redirect HTTP to HTTPS (recommended)

# Auto-renewal is configured automatically
# Test renewal:
certbot renew --dry-run
```

---

## Step 6: Verify Everything Works

### Check DNS:
```bash
# On your local machine or server
nslookup charmstracker.com
# Should return: 31.220.50.205

nslookup www.charmstracker.com
# Should return: 31.220.50.205
```

### Test in Browser:
1. **Frontend:** http://charmstracker.com
2. **Frontend (www):** http://www.charmstracker.com
3. **API:** http://31.220.50.205/api/
4. **API Test:** http://31.220.50.205/api/charms

### Check Nginx:
```bash
# View logs
tail -f /var/log/nginx/charmstracker_frontend_access.log
tail -f /var/log/nginx/charmstracker_api_access.log

# Check status
systemctl status nginx
```

---

## Complete Deployment Commands (After DNS is Set)

```bash
# 1. Update backend .env
nano /root/Charmstracker/backend/.env
# Add CORS_ORIGINS with your domain

# 2. Restart backend
systemctl restart charmstracker-api

# 3. Update nginx configs
cp /root/Charmstracker/nginx_api.conf /etc/nginx/sites-available/charmstracker-api
cp /root/Charmstracker/nginx_frontend.conf /etc/nginx/sites-available/charmstracker-frontend

# 4. Test and reload nginx
nginx -t
systemctl reload nginx

# 5. Setup SSL (after DNS works)
certbot --nginx -d charmstracker.com -d www.charmstracker.com

# 6. Rebuild frontend with correct API URL
cd /root/Charmstracker/frontend
nano src/services/api.js  # Update API_BASE_URL
yarn build
systemctl reload nginx
```

---

## After SSL is Setup

Your URLs will be:
- **Frontend:** https://charmstracker.com ✅
- **Frontend (www):** https://www.charmstracker.com ✅
- **API:** http://31.220.50.205/api/ ✅

**Note:** You can also get SSL for the API IP later by using a subdomain like `api.charmstracker.com`

---

## Optional: Setup API Subdomain

If you want `api.charmstracker.com` instead of IP:

### DNS Record:
```
Type: A
Name: api
Value: 31.220.50.205
```

### Update nginx_api.conf:
```nginx
server_name api.charmstracker.com 31.220.50.205;
```

### Get SSL:
```bash
certbot --nginx -d api.charmstracker.com
```

### Update frontend API URL:
```javascript
const API_BASE_URL = 'https://api.charmstracker.com/api';
```

---

## Troubleshooting

### DNS not working:
```bash
# Check DNS propagation
# Visit: https://dnschecker.org/
# Enter: charmstracker.com

# Clear local DNS cache (Windows):
ipconfig /flushdns

# Wait 1-2 hours for propagation
```

### Nginx errors:
```bash
nginx -t
tail -f /var/log/nginx/error.log
systemctl status nginx
```

### CORS errors:
```bash
# Check backend .env has correct domains
cat /root/Charmstracker/backend/.env

# Restart backend
systemctl restart charmstracker-api
```

### SSL certificate issues:
```bash
# Check certificate status
certbot certificates

# Renew certificate
certbot renew

# Force renew
certbot renew --force-renewal
```

---

## Summary

1. ✅ Set up DNS A records for charmstracker.com → 31.220.50.205
2. ✅ Update backend CORS to allow charmstracker.com
3. ✅ Upload new nginx configs
4. ✅ Update frontend API URL to use IP address
5. ✅ Get SSL certificate with Certbot
6. ✅ Test everything works

**Timeline:**
- DNS setup: 5 mins
- DNS propagation: 1-2 hours
- SSL setup: 5 mins (after DNS works)
- Total: ~2 hours
