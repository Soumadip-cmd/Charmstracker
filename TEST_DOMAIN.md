# Test CharmTracker.com Domain

## Commands to run on your Hostinger server:

```bash
# 1. Check DNS resolution
nslookup charmstracker.com
nslookup www.charmstracker.com

# 2. Test frontend via domain
curl -I http://charmstracker.com
curl -I http://www.charmstracker.com

# 3. Test if you can access the HTML
curl http://charmstracker.com
curl http://www.charmstracker.com

# 4. Test API via domain (if you want API on domain too)
curl http://charmstracker.com/api/
curl http://charmstracker.com/api/charms

# 5. Check Nginx access logs
tail -f /var/log/nginx/charmstracker_frontend_access.log
# Press Ctrl+C to exit

# 6. Check for any errors
tail -f /var/log/nginx/error.log
# Press Ctrl+C to exit
```

## If DNS is working, you should see:

```bash
nslookup charmstracker.com
# Should return: 31.220.50.205
```

## Access in Browser:

Once DNS propagates (1-2 hours):
- Frontend: http://charmstracker.com
- Frontend: http://www.charmstracker.com
- API: http://31.220.50.205/api/

## If DNS not working yet:

You can test with the IP directly:
```bash
curl -H "Host: charmstracker.com" http://31.220.50.205
```

## Check what domains Nginx is listening for:

```bash
cat /etc/nginx/sites-enabled/charmstracker-frontend | grep server_name
cat /etc/nginx/sites-enabled/charmstracker-api | grep server_name
```
