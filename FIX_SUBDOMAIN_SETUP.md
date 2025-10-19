# Fix Subdomain Setup - Quick Guide

## 🚨 Current Issues:
1. ✅ SSL certificate obtained for charms.freelixe.com
2. ❌ Certbot couldn't auto-configure (missing server_name match)
3. ❌ Git merge conflict with frontend/.env.production
4. ❌ Nginx conflicting server names

---

## 🔧 Fix Everything (Run on Server):

```bash
# Step 1: Stash local changes
cd /root/Charmstracker
git stash

# Step 2: Pull latest code
git pull origin main

# Step 3: Re-copy configs
cp nginx_api.conf /etc/nginx/sites-available/charmstracker-api
cp nginx_frontend.conf /etc/nginx/sites-available/charmstracker-frontend

# Step 4: Manually add SSL to API config
cat > /etc/nginx/sites-available/charmstracker-api << 'EOF'
server {
    listen 80;
    server_name charms.freelixe.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name charms.freelixe.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/charms.freelixe.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/charms.freelixe.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # API endpoint
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Root endpoint
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Error logs
    error_log /var/log/nginx/charmstracker_api_error.log;
    access_log /var/log/nginx/charmstracker_api_access.log;
}
EOF

# Step 5: Add SSL to frontend config (use certbot)
certbot --nginx -d charmstracker.com -d www.charmstracker.com

# Step 6: Test and restart
nginx -t
systemctl restart nginx
systemctl restart charmstracker-api

# Step 7: Test API
echo "Testing API..."
curl https://charms.freelixe.com/api/
curl https://charms.freelixe.com/api/charms

# Step 8: Test Frontend
echo "Testing Frontend..."
curl -I https://charmstracker.com
```

---

## 📋 All-in-One Command:

```bash
cd /root/Charmstracker && \
git stash && \
git pull origin main && \
cp nginx_api.conf /etc/nginx/sites-available/charmstracker-api && \
cp nginx_frontend.conf /etc/nginx/sites-available/charmstracker-frontend && \
cat > /etc/nginx/sites-available/charmstracker-api << 'EOF'
server {
    listen 80;
    server_name charms.freelixe.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name charms.freelixe.com;

    ssl_certificate /etc/letsencrypt/live/charms.freelixe.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/charms.freelixe.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    error_log /var/log/nginx/charmstracker_api_error.log;
    access_log /var/log/nginx/charmstracker_api_access.log;
}
EOF

certbot --nginx -d charmstracker.com -d www.charmstracker.com && \
nginx -t && \
systemctl restart nginx && \
systemctl restart charmstracker-api && \
echo "" && \
echo "✅ Testing API..." && \
curl https://charms.freelixe.com/api/ && \
echo "" && \
echo "✅ Testing Frontend..." && \
curl -I https://charmstracker.com
```

---

## 🧪 Final Tests:

```bash
# Check nginx is listening on both ports
netstat -tlnp | grep nginx

# Should see:
# 0.0.0.0:80
# 0.0.0.0:443

# Test API
curl https://charms.freelixe.com/api/
curl https://charms.freelixe.com/api/charms

# Test Frontend
curl https://charmstracker.com

# Check services
systemctl status nginx --no-pager
systemctl status charmstracker-api --no-pager
```

---

## 🌐 Expected URLs:

**Frontend:** https://charmstracker.com  
**API:** https://charms.freelixe.com/api/

---

## 📝 What This Does:

1. ✅ Resolves git merge conflict (stash changes)
2. ✅ Pulls latest code
3. ✅ Manually configures SSL for API subdomain
4. ✅ Uses certbot to configure SSL for frontend
5. ✅ Restarts all services
6. ✅ Tests both domains

The key fix: **Manually add SSL directives** to the API config since certbot couldn't auto-detect the server block.
