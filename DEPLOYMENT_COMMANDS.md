# CharmTracker Deployment Commands for Hostinger

## Server IP: 31.220.50.205

---

## 1. Initial Server Setup

```bash
# SSH into your Hostinger VPS
ssh root@31.220.50.205

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y nginx python3 python3-pip python3-venv nodejs npm git
```

---

## 2. Install MongoDB

```bash
# Import MongoDB public GPG key
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor

# Create MongoDB list file
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Update package database
sudo apt update

# Install MongoDB
sudo apt install -y mongodb-org

# Start and enable MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify MongoDB is running
sudo systemctl status mongod
```

---

## 3. Setup Application Directory

```bash
# Your application is already at: /root/Charmstracker
cd /root/Charmstracker

# If you need to clone fresh:
# git clone https://github.com/carefreelixe-cmd/Charmstracker.git /root/Charmstracker

# Or upload files manually using SCP from your local machine:
# scp -r D:\Charmstracker/* root@31.220.50.205:/root/Charmstracker/
```

---

## 4. Setup Backend (API)

```bash
# Navigate to backend directory
cd /var/www/charmstracker/backend

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create .env file (edit with your MongoDB credentials)
nano .env
```

### Backend .env file content:
```env
MONGO_URL=mongodb://localhost:27017/
DB_NAME=charmstracker
CORS_ORIGINS=http://31.220.50.205,http://www.31.220.50.205
```

```bash
# Save and exit (Ctrl+X, Y, Enter)

# Test the backend
uvicorn backend.server:app --host 127.0.0.1 --port 8000

# Press Ctrl+C to stop, then create systemd service
```

---

## 5. Create Backend Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/charmstracker-api.service
```

### Service file content:
```ini
[Unit]
Description=CharmTracker FastAPI Application
After=network.target mongodb.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/charmstracker
Environment="PATH=/var/www/charmstracker/backend/venv/bin"
ExecStart=/var/www/charmstracker/backend/venv/bin/uvicorn backend.server:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Save and exit (Ctrl+X, Y, Enter)

# Set proper permissions
sudo chown -R www-data:www-data /var/www/charmstracker

# Reload systemd, enable and start service
sudo systemctl daemon-reload
sudo systemctl enable charmstracker-api
sudo systemctl start charmstracker-api

# Check service status
sudo systemctl status charmstracker-api
```

---

## 6. Setup Frontend

```bash
# Navigate to frontend directory
cd /var/www/charmstracker/frontend

# Install dependencies
npm install

# Create production build
npm run build

# The build folder will contain the production-ready files
```

---

## 7. Configure Nginx

```bash
# Copy API nginx config
sudo cp /var/www/charmstracker/nginx_api.conf /etc/nginx/sites-available/charmstracker-api

# Copy Frontend nginx config
sudo cp /var/www/charmstracker/nginx_frontend.conf /etc/nginx/sites-available/charmstracker-frontend

# Create symbolic links to enable sites
sudo ln -s /etc/nginx/sites-available/charmstracker-api /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/charmstracker-frontend /etc/nginx/sites-enabled/

# Remove default nginx site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# If test is successful, reload nginx
sudo systemctl reload nginx
sudo systemctl restart nginx

# Enable nginx to start on boot
sudo systemctl enable nginx
```

---

## 8. Setup Firewall

```bash
# Allow SSH (important - don't lock yourself out!)
sudo ufw allow 22/tcp

# Allow HTTP
sudo ufw allow 80/tcp

# Allow HTTPS (for future SSL setup)
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw --force enable

# Check firewall status
sudo ufw status
```

---

## 9. Seed Database (Optional)

```bash
# Navigate to backend directory
cd /var/www/charmstracker/backend

# Activate virtual environment
source venv/bin/activate

# Run seed script
python seed_data.py

# Deactivate virtual environment
deactivate
```

---

## 10. Verify Deployment

```bash
# Check if API is running
curl http://127.0.0.1:8000/api/

# Check if MongoDB is running
sudo systemctl status mongod

# Check if backend service is running
sudo systemctl status charmstracker-api

# Check if Nginx is running
sudo systemctl status nginx

# View API logs
sudo journalctl -u charmstracker-api -f

# View Nginx logs
sudo tail -f /var/log/nginx/charmstracker_api_access.log
sudo tail -f /var/log/nginx/charmstracker_api_error.log
sudo tail -f /var/log/nginx/charmstracker_frontend_access.log
sudo tail -f /var/log/nginx/charmstracker_frontend_error.log
```

---

## 11. Access Your Application

- **API**: http://31.220.50.205/api/
- **Frontend**: http://www.31.220.50.205 or http://31.220.50.205

---

## 12. Useful Management Commands

```bash
# Restart backend service
sudo systemctl restart charmstracker-api

# View backend logs
sudo journalctl -u charmstracker-api -f

# Restart nginx
sudo systemctl restart nginx

# Test nginx config
sudo nginx -t

# Reload nginx (without downtime)
sudo systemctl reload nginx

# Restart MongoDB
sudo systemctl restart mongod

# Check MongoDB status
sudo systemctl status mongod

# Update application code
cd /var/www/charmstracker
git pull origin main

# Rebuild frontend after code update
cd frontend
npm install
npm run build

# Restart services after update
sudo systemctl restart charmstracker-api
sudo systemctl reload nginx
```

---

## 13. SSL Certificate Setup (Optional - Recommended)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain if you have one)
# For now, you can skip this and use HTTP
# When you have a domain name:
# sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 14. Troubleshooting

```bash
# If backend service fails
sudo journalctl -u charmstracker-api -n 50 --no-pager

# If nginx fails
sudo nginx -t
sudo tail -f /var/log/nginx/error.log

# Check if port 8000 is in use
sudo netstat -tlnp | grep 8000

# Check if MongoDB is accessible
mongo --eval "db.stats()"

# Fix permissions if needed
sudo chown -R www-data:www-data /var/www/charmstracker
sudo chmod -R 755 /var/www/charmstracker
```

---

## Notes

1. **Security**: This is a basic setup. For production, you should:
   - Set up SSL/TLS certificates
   - Configure MongoDB authentication
   - Set up proper firewall rules
   - Use environment variables for sensitive data
   - Set up regular backups

2. **Domain Name**: If you get a domain name, update the `server_name` in nginx configs

3. **MongoDB Atlas**: Consider using MongoDB Atlas for production instead of local MongoDB

4. **Monitoring**: Set up monitoring tools like PM2, New Relic, or DataDog

5. **Backup**: Regularly backup your MongoDB database:
   ```bash
   mongodump --db charmstracker --out /backup/mongodb/$(date +%Y%m%d)
   ```
