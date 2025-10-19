# Debug API Not Working

## Run these commands on server to diagnose:

```bash
# 1. Check backend is running
systemctl status charmstracker-api --no-pager

# 2. Test backend directly (bypass nginx)
curl http://127.0.0.1:8000/api/charms

# 3. Check nginx API config
cat /etc/nginx/sites-enabled/charmstracker-api

# 4. Check nginx frontend config
cat /etc/nginx/sites-enabled/charmstracker-frontend | grep "location /api"

# 5. Test with specific host header
curl -H "Host: charmstracker.com" https://charmstracker.com/api/charms

# 6. Check nginx error logs
tail -n 50 /var/log/nginx/error.log

# 7. Check which nginx sites are enabled
ls -la /etc/nginx/sites-enabled/

# 8. Test nginx config
nginx -t
```

## Quick Fix - Run This:

```bash
# Remove the API redirect and let backend handle it
systemctl restart charmstracker-api

# Test backend directly
curl http://127.0.0.1:8000/api/charms

# If backend works, the issue is nginx routing
# Check which config is handling the request
nginx -T | grep -A 20 "server_name.*charmstracker"
```

## Show me the output of:
```bash
systemctl status charmstracker-api --no-pager
curl http://127.0.0.1:8000/api/charms
cat /etc/nginx/sites-enabled/charmstracker-frontend | grep -A 10 "location /api"
```
