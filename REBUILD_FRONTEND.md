# Rebuild Frontend - Complete Reset

## Run these commands on your Hostinger server:

```bash
# 1. Stash local changes
cd /root/Charmstracker
git stash

# 2. Pull latest code
git pull origin main

# 3. Navigate to frontend
cd frontend

# 4. Clean old build
rm -rf build node_modules

# 5. Install dependencies
yarn install

# 6. Build production version
yarn build

# 7. Verify build was created
ls -la build/

# 8. Check if index.html exists
ls -la build/index.html

# 9. Restart services
systemctl restart nginx

# 10. Test
curl -I http://charmstracker.com
```

## All in one command:

```bash
cd /root/Charmstracker && \
git stash && \
git pull origin main && \
cd frontend && \
rm -rf build node_modules && \
yarn install && \
yarn build && \
ls -la build/ && \
systemctl restart nginx && \
echo "✅ Frontend rebuilt successfully!" && \
curl -I http://charmstracker.com
```

## If you want to completely reset everything:

```bash
# Backup current setup
cd /root
mv Charmstracker Charmstracker_backup

# Clone fresh
git clone https://github.com/carefreelixe-cmd/Charmstracker.git
cd Charmstracker

# Build frontend
cd frontend
yarn install
yarn build

# Setup backend (if needed)
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
cat > .env << 'EOF'
MONGO_URL="mongodb+srv://carefreelixe_db_user:d9po0rKPJwchyCBE@laundry.bhx3jw0.mongodb.net/?retryWrites=true&w=majority"
DB_NAME="charmtracker_production"
CORS_ORIGINS="http://charmstracker.com,http://www.charmstracker.com,https://charmstracker.com,https://www.charmstracker.com,http://31.220.50.205"
EOF

deactivate

# Restart services
systemctl restart charmstracker-api
systemctl restart nginx

# Test
curl http://charmstracker.com
curl http://31.220.50.205/api/charms
```

## Quick rebuild (recommended):

```bash
cd /root/Charmstracker
git stash
git pull
cd frontend
rm -rf build
yarn build
systemctl restart nginx
curl -I http://charmstracker.com
```
