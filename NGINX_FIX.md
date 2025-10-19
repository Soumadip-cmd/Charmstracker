# Quick Fix for Nginx 404 Error

## The Issue:
- API works locally: ✅ http://127.0.0.1:8000/api/
- API doesn't work via IP: ❌ http://31.220.50.205/api/

## Solution: Enable the Nginx sites

Run these commands on your server:

```bash
# Check if symbolic links exist
ls -la /etc/nginx/sites-enabled/

# Remove any existing links
rm -f /etc/nginx/sites-enabled/charmstracker-api
rm -f /etc/nginx/sites-enabled/charmstracker-frontend

# Create new symbolic links
ln -s /etc/nginx/sites-available/charmstracker-api /etc/nginx/sites-enabled/charmstracker-api
ln -s /etc/nginx/sites-available/charmstracker-frontend /etc/nginx/sites-enabled/charmstracker-frontend

# Remove default nginx site if it exists
rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
nginx -t

# Restart nginx
systemctl restart nginx

# Test API again
curl http://31.220.50.205/api/
curl http://31.220.50.205/api/charms
```

## If still getting 404, check this:

```bash
# View nginx error logs
tail -f /var/log/nginx/error.log

# Check what sites are enabled
ls -la /etc/nginx/sites-enabled/

# Check nginx configuration files
cat /etc/nginx/sites-available/charmstracker-api
cat /etc/nginx/sites-available/charmstracker-frontend

# Restart everything
systemctl restart charmstracker-api
systemctl restart nginx

# Check if port 8000 is listening
netstat -tlnp | grep 8000
```

## Verify Services

```bash
# Check backend is running
systemctl status charmstracker-api

# Check nginx is running
systemctl status nginx

# Test backend directly
curl http://127.0.0.1:8000/api/charms
```
