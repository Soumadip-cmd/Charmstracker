# Fix Environment Variables

## ✅ Updated .env to use HTTPS domain

Now push and rebuild:

### Step 1: Push to GitHub (Windows):
```powershell
cd D:\Charmstracker
git add .
git commit -m "Update env to use HTTPS domain"
git push origin main
```

### Step 2: On Server - Create .env.production:
```bash
# Create production env file
cat > /root/Charmstracker/frontend/.env.production << 'EOF'
REACT_APP_BACKEND_URL=https://charmstracker.com
EOF

# Pull latest changes
cd /root/Charmstracker
git pull origin main

# Copy .env to .env.production (backup)
cp frontend/.env frontend/.env.production

# Rebuild
cd frontend
rm -rf build
yarn build

# Restart
systemctl restart nginx

# Test
curl https://charmstracker.com/api/charms
```

### All-in-One Command (Server):
```bash
cat > /root/Charmstracker/frontend/.env.production << 'EOF'
REACT_APP_BACKEND_URL=https://charmstracker.com
EOF

cd /root/Charmstracker && \
git pull origin main && \
cd frontend && \
rm -rf build && \
yarn build && \
systemctl restart nginx && \
echo "✅ Done! Open https://charmstracker.com"
```

### Test API:
```bash
# Should return JSON data, not HTML redirect
curl https://charmstracker.com/api/charms

# Check backend status
systemctl status charmstracker-api --no-pager
```
