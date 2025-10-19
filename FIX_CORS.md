# Fix CORS Error - Commands to Run

## The Problem:
Both Nginx and FastAPI are adding CORS headers, causing duplicates.

## Solution:
Remove CORS headers from Nginx and let FastAPI handle them.

## Commands to run on your server:

```bash
# 1. Upload the fixed nginx config from Windows
# (Run this in PowerShell on Windows)
scp D:\Charmstracker\nginx_api.conf root@31.220.50.205:/root/Charmstracker/
```

## Then on your Hostinger server:

```bash
# 2. Copy the fixed config
cp /root/Charmstracker/nginx_api.conf /etc/nginx/sites-available/charmstracker-api

# 3. Test nginx config
nginx -t

# 4. Restart nginx
systemctl restart nginx

# 5. Restart backend (just to be safe)
systemctl restart charmstracker-api

# 6. Check services
systemctl status nginx --no-pager
systemctl status charmstracker-api --no-pager

# 7. Test CORS
curl -I http://31.220.50.205/api/charms

# 8. View logs if needed
journalctl -u charmstracker-api -n 20 --no-pager
```

## All in one command:

```bash
cp /root/Charmstracker/nginx_api.conf /etc/nginx/sites-available/charmstracker-api && \
nginx -t && \
systemctl restart nginx && \
systemctl restart charmstracker-api && \
echo "✅ Services restarted!" && \
sleep 2 && \
curl -I http://31.220.50.205/api/charms
```

## Verify CORS headers:

```bash
# Should only show ONE Access-Control-Allow-Origin header
curl -I http://31.220.50.205/api/charms | grep -i "access-control"
```

## Expected result:
You should see:
```
access-control-allow-origin: http://charmstracker.com
```
Or:
```
access-control-allow-origin: *
```

But NOT both!
