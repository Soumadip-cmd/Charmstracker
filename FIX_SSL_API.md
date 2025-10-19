# Quick Fix for SSL Error

## The Problem:
Nginx can't start because SSL is enabled but certificates aren't specified.

## ✅ Solution: Let Certbot Handle API SSL

Since your frontend already has SSL from certbot, we'll let it handle the API too.

---

## 🚀 Run These Commands on Server:

```bash
# 1. Pull latest fixed config
cd /root/Charmstracker
git pull origin main

# 2. Apply API config
cp nginx_api.conf /etc/nginx/sites-available/charmstracker-api

# 3. Check if certbot already configured frontend
cat /etc/nginx/sites-available/charmstracker-frontend | grep ssl_certificate

# 4. Run certbot to add API to existing certificate
certbot --nginx -d charmstracker.com -d www.charmstracker.com

# 5. Test nginx
nginx -t

# 6. Restart nginx
systemctl restart nginx

# 7. Rebuild frontend
cd /root/Charmstracker/frontend
rm -rf build
yarn build

# 8. Restart nginx again
systemctl restart nginx

# 9. Test
curl https://charmstracker.com/api/
curl https://charmstracker.com/api/charms
```

---

## 📋 All-in-One Command:

```bash
cd /root/Charmstracker && \
git pull origin main && \
cp nginx_api.conf /etc/nginx/sites-available/charmstracker-api && \
certbot --nginx -d charmstracker.com -d www.charmstracker.com && \
nginx -t && \
systemctl restart nginx && \
cd frontend && \
rm -rf build && \
yarn build && \
systemctl restart nginx && \
echo "✅ Testing..." && \
curl https://charmstracker.com/api/charms
```

---

## 🔍 If Certbot Asks Questions:

1. **Renew existing certificate?** → Yes (1)
2. **Redirect HTTP to HTTPS?** → Yes (2)

---

## ✅ After This:

Your API will be available at:
- ✅ https://charmstracker.com/api/
- ✅ https://charmstracker.com/api/charms
- ✅ https://www.charmstracker.com/api/

Frontend will load data successfully! 🎉
