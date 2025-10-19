# Setup API on Subdomain charms.freelixe.com

## ✅ Configuration Updated

**Frontend Domain:** charmstracker.com  
**API Domain:** charms.freelixe.com

---

## 🌐 Step 1: Setup DNS (Do This First!)

Go to your domain registrar and add this A record:

```
Type: A
Name: charms
Domain: freelixe.com
Value: 31.220.50.205
TTL: 3600
```

This creates: **charms.freelixe.com** → 31.220.50.205

Wait 5-15 minutes for DNS to propagate.

Check: `nslookup charms.freelixe.com`

---

## 🚀 Step 2: Push Changes to GitHub (Windows)

```powershell
cd D:\Charmstracker
git add .
git commit -m "Setup API on subdomain charms.freelixe.com"
git push origin main
```

---

## 🚀 Step 3: Deploy on Server

```bash
# Pull latest code
cd /root/Charmstracker
git pull origin main

# Update backend .env
cp backend/.env.production backend/.env
# Or manually create:
cat > /root/Charmstracker/backend/.env << 'EOF'
MONGO_URL="mongodb+srv://carefreelixe_db_user:d9po0rKPJwchyCBE@laundry.bhx3jw0.mongodb.net/?retryWrites=true&w=majority"
DB_NAME="charmtracker_production"
CORS_ORIGINS="http://charmstracker.com,http://www.charmstracker.com,https://charmstracker.com,https://www.charmstracker.com,https://charms.freelixe.com,http://localhost:3000"
EOF

# Update nginx configs
cp nginx_api.conf /etc/nginx/sites-available/charmstracker-api
cp nginx_frontend.conf /etc/nginx/sites-available/charmstracker-frontend

# Enable API config
ln -sf /etc/nginx/sites-available/charmstracker-api /etc/nginx/sites-enabled/charmstracker-api

# Test nginx
nginx -t

# Restart services
systemctl restart charmstracker-api
systemctl restart nginx

# Create frontend production env
cat > /root/Charmstracker/frontend/.env.production << 'EOF'
REACT_APP_BACKEND_URL=https://charms.freelixe.com
EOF

# Rebuild frontend
cd frontend
rm -rf build
yarn build

# Restart nginx
systemctl restart nginx
```

---

## 🔒 Step 4: Setup SSL for API Subdomain

```bash
# Get SSL certificate for API subdomain
certbot --nginx -d charms.freelixe.com

# Follow prompts:
# - Enter email
# - Agree to terms
# - Redirect HTTP to HTTPS: Yes (2)
```

---

## 📋 All-in-One Command (After DNS is set):

```bash
cd /root/Charmstracker && \
git pull origin main && \
cat > backend/.env << 'EOF'
MONGO_URL="mongodb+srv://carefreelixe_db_user:d9po0rKPJwchyCBE@laundry.bhx3jw0.mongodb.net/?retryWrites=true&w=majority"
DB_NAME="charmtracker_production"
CORS_ORIGINS="https://charmstracker.com,https://www.charmstracker.com,https://charms.freelixe.com"
EOF

cp nginx_api.conf /etc/nginx/sites-available/charmstracker-api && \
cp nginx_frontend.conf /etc/nginx/sites-available/charmstracker-frontend && \
ln -sf /etc/nginx/sites-available/charmstracker-api /etc/nginx/sites-enabled/charmstracker-api && \
nginx -t && \
systemctl restart charmstracker-api && \
systemctl restart nginx && \
cat > frontend/.env.production << 'EOF'
REACT_APP_BACKEND_URL=https://charms.freelixe.com
EOF

cd frontend && \
rm -rf build && \
yarn build && \
systemctl restart nginx && \
echo "✅ Setup complete!"
```

---

## ✅ Step 5: Get SSL Certificate

```bash
certbot --nginx -d charms.freelixe.com
```

---

## 🧪 Test Everything

```bash
# Test API
curl https://charms.freelixe.com/api/
curl https://charms.freelixe.com/api/charms

# Test frontend
curl -I https://charmstracker.com

# Check services
systemctl status charmstracker-api --no-pager
systemctl status nginx --no-pager
```

---

## 🌐 Final URLs

**Frontend:** https://charmstracker.com  
**API:** https://charms.freelixe.com/api/

---

## 📝 Summary

1. ✅ Add DNS: charms.freelixe.com → 31.220.50.205
2. ✅ Push code to GitHub
3. ✅ Deploy on server
4. ✅ Get SSL certificate
5. ✅ Test and enjoy!

Clean separation: Frontend and API on different domains! 🎉
