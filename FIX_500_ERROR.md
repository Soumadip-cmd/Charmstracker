# Fix 500 Internal Server Error

## The Issue:
✅ DNS is working (charmstracker.com → 31.220.50.205)
✅ Nginx config is correct
❌ 500 Internal Server Error (likely permissions issue)

## Run these commands on your server:

```bash
# 1. Check Nginx error log to see the exact error
tail -n 50 /var/log/nginx/error.log

# 2. Fix permissions on frontend build folder
chmod -R 755 /root/Charmstracker/frontend/build
chmod -R 755 /root/Charmstracker

# 3. Make sure the build folder exists
ls -la /root/Charmstracker/frontend/build/

# 4. Check if index.html exists
ls -la /root/Charmstracker/frontend/build/index.html

# 5. Alternative: Change Nginx user to root
# Edit nginx.conf
nano /etc/nginx/nginx.conf
# Change the first line from:
# user www-data;
# To:
# user root;
# Save with Ctrl+X, Y, Enter

# 6. Test nginx config
nginx -t

# 7. Restart nginx
systemctl restart nginx

# 8. Test again
curl -I http://charmstracker.com
curl http://charmstracker.com
```

## Quick Fix (All in one):

```bash
# Fix permissions and restart
chmod -R 755 /root/Charmstracker && \
sed -i 's/user www-data;/user root;/' /etc/nginx/nginx.conf && \
nginx -t && \
systemctl restart nginx && \
curl -I http://charmstracker.com
```

## Alternative: Move build to /var/www

If you prefer not to run Nginx as root:

```bash
# Create directory
mkdir -p /var/www/charmstracker

# Copy build files
cp -r /root/Charmstracker/frontend/build /var/www/charmstracker/

# Set ownership
chown -R www-data:www-data /var/www/charmstracker

# Update nginx config
nano /etc/nginx/sites-available/charmstracker-frontend
# Change: root /root/Charmstracker/frontend/build;
# To:     root /var/www/charmstracker/build;

# Reload nginx
nginx -t
systemctl reload nginx
```

## Check what the actual error is:

```bash
tail -f /var/log/nginx/error.log
# Then visit http://charmstracker.com in browser or curl
# See what error appears in the log
```
