#!/bin/bash
# CharmTracker Backend Setup Script
# Run this on your Hostinger server

echo "========================================="
echo "CharmTracker Backend Setup"
echo "========================================="
echo ""

# 1. Setup Python Virtual Environment
echo "Step 1: Setting up Python virtual environment..."
cd /root/Charmstracker/backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

echo "Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
deactivate

echo "✓ Virtual environment setup complete"
echo ""

# 2. Create .env file
echo "Step 2: Creating .env file..."
cat > /root/Charmstracker/backend/.env << 'EOF'
MONGO_URL=mongodb://localhost:27017/
DB_NAME=charmstracker
CORS_ORIGINS=http://charmstracker.com,http://www.charmstracker.com,https://charmstracker.com,https://www.charmstracker.com,http://31.220.50.205
EOF

echo "✓ .env file created"
echo ""

# 3. Check MongoDB
echo "Step 3: Checking MongoDB..."
if systemctl is-active --quiet mongod; then
    echo "✓ MongoDB is running"
else
    echo "MongoDB is not running. Starting MongoDB..."
    systemctl start mongod
    systemctl enable mongod
    if systemctl is-active --quiet mongod; then
        echo "✓ MongoDB started successfully"
    else
        echo "⚠ Warning: MongoDB failed to start. You may need to install it."
        echo "Run: apt update && apt install -y mongodb-org"
    fi
fi
echo ""

# 4. Copy systemd service file
echo "Step 4: Installing systemd service..."
cp /root/Charmstracker/charmstracker-api.service /etc/systemd/system/
systemctl daemon-reload
echo "✓ Service file installed"
echo ""

# 5. Enable and start service
echo "Step 5: Starting backend service..."
systemctl enable charmstracker-api
systemctl start charmstracker-api

# Wait a moment for service to start
sleep 2

if systemctl is-active --quiet charmstracker-api; then
    echo "✓ Backend service started successfully"
else
    echo "⚠ Warning: Backend service failed to start"
    echo "Check logs with: journalctl -u charmstracker-api -n 50"
fi
echo ""

# 6. Test API
echo "Step 6: Testing API..."
sleep 2
if curl -s http://127.0.0.1:8000/api/ > /dev/null; then
    echo "✓ API is responding"
else
    echo "⚠ Warning: API is not responding"
fi
echo ""

# 7. Reload Nginx
echo "Step 7: Reloading Nginx..."
systemctl reload nginx
echo "✓ Nginx reloaded"
echo ""

echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Check status with:"
echo "  systemctl status charmstracker-api"
echo "  systemctl status nginx"
echo "  systemctl status mongod"
echo ""
echo "View logs with:"
echo "  journalctl -u charmstracker-api -f"
echo ""
echo "Test API:"
echo "  curl http://127.0.0.1:8000/api/"
echo "  curl http://31.220.50.205/api/"
echo ""
echo "Access your app:"
echo "  Frontend: http://charmstracker.com"
echo "  API: http://31.220.50.205/api/"
echo ""
