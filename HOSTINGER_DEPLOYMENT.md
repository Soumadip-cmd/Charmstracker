# 🚀 CharmTracker Backend Deployment Guide for Hostinger

## 📋 Prerequisites
- Hostinger Python hosting account
- MongoDB Atlas account (free tier available at mongodb.com/cloud/atlas)
- Your GitHub repository

---

## 🔧 Backend Setup Instructions

### 1. **Entry Point File**
**File:** `backend/server.py`

This is your main application file that Hostinger will use to start your backend.

### 2. **Start Command for Hostinger**
Use this command in your Hostinger Python app settings:

```bash
uvicorn backend.server:app --host 0.0.0.0 --port 8000
```

**OR** if Hostinger uses a different structure:

```bash
cd backend && uvicorn server:app --host 0.0.0.0 --port 8000
```

### 3. **Alternative: Using Gunicorn (Recommended for Production)**
If Hostinger supports Gunicorn:

```bash
gunicorn backend.server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 📦 Dependencies Installation

### **Python Version Required:** 3.9+

### **Main Dependencies File:** `backend/requirements.txt`

All dependencies are already listed in `/app/backend/requirements.txt`. Hostinger should automatically install them, but if you need to install manually:

```bash
pip install -r backend/requirements.txt
```

### **Key Dependencies:**
- fastapi==0.110.1
- uvicorn==0.25.0
- motor==3.3.1 (MongoDB async driver)
- pymongo==4.5.0
- pydantic>=2.6.4
- python-dotenv>=1.0.1

---

## 🗄️ Database Setup (MongoDB Atlas)

### Step 1: Create MongoDB Atlas Database
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free tier (512MB storage)
3. Create a new cluster
4. Click "Connect" → "Connect your application"
5. Copy your connection string (looks like):
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### Step 2: Update Environment Variables
Update `backend/.env` with your MongoDB Atlas connection:

```env
MONGO_URL="mongodb+srv://your-username:your-password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
DB_NAME="charmtracker_production"
CORS_ORIGINS="https://yourdomain.com,https://www.yourdomain.com"
```

### Step 3: Seed Your Database
After deploying, run this once to populate with sample data:

```bash
python backend/seed_data.py
```

---

## 🌐 Hostinger Configuration

### **Directory Structure on Hostinger:**
```
/home/username/htdocs/
├── backend/
│   ├── server.py          ← Entry point
│   ├── .env               ← Environment variables
│   ├── requirements.txt   ← Dependencies
│   ├── models/
│   ├── routes/
│   └── seed_data.py
└── frontend/
    └── build/             ← React production build
```

### **Application Settings in Hostinger Panel:**

1. **Application Root:** `/home/username/htdocs`

2. **Entry Point:** `backend/server.py`

3. **Application Startup File:** `server.py`

4. **Start Command:**
   ```bash
   uvicorn backend.server:app --host 0.0.0.0 --port 8000
   ```

5. **Python Version:** 3.9 or higher

6. **Environment Variables** (Set these in Hostinger control panel):
   - `MONGO_URL`: Your MongoDB Atlas connection string
   - `DB_NAME`: charmtracker_production
   - `CORS_ORIGINS`: https://yourdomain.com
   - `PORT`: 8000 (or whatever Hostinger assigns)

---

## 🔄 Alternative Deployment Options

### **Option 1: Using Passenger (if Hostinger uses it)**
Create `passenger_wsgi.py` in root directory:

```python
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from backend.server import app as application
```

### **Option 2: Using a startup script**
Create `start.sh`:

```bash
#!/bin/bash
cd /home/username/htdocs
source venv/bin/activate
cd backend
uvicorn server:app --host 0.0.0.0 --port 8000 --workers 4
```

Make it executable:
```bash
chmod +x start.sh
```

---

## 🧪 Testing Your Deployment

### 1. **Test Backend Health:**
```bash
curl https://your-hostinger-domain.com/api/
```

Expected response:
```json
{"message": "CharmTracker API is running"}
```

### 2. **Test Charms Endpoint:**
```bash
curl https://your-hostinger-domain.com/api/charms?page=1&limit=5
```

### 3. **Test Trending Endpoint:**
```bash
curl https://your-hostinger-domain.com/api/trending
```

---

## 🚨 Troubleshooting

### **Issue: Module Not Found**
**Solution:** Ensure all dependencies are installed:
```bash
pip install -r backend/requirements.txt
```

### **Issue: Database Connection Failed**
**Solution:** 
1. Check MONGO_URL in .env is correct
2. Whitelist Hostinger IP in MongoDB Atlas → Network Access
3. Or whitelist all IPs: 0.0.0.0/0

### **Issue: CORS Errors**
**Solution:** Update CORS_ORIGINS in backend/.env:
```env
CORS_ORIGINS="*"  # For testing
# OR
CORS_ORIGINS="https://yourdomain.com,https://www.yourdomain.com"
```

### **Issue: Port Already in Use**
**Solution:** Use Hostinger's assigned port or change in start command

---

## 📱 Frontend Deployment

### **For React Frontend on Hostinger:**

1. **Build the frontend locally:**
   ```bash
   cd frontend
   yarn build
   ```

2. **Upload `build/` folder to Hostinger public_html**

3. **Update `frontend/.env` before building:**
   ```env
   REACT_APP_BACKEND_URL=https://your-backend-domain.com
   ```

4. **Create `.htaccess` in public_html:**
   ```apache
   <IfModule mod_rewrite.c>
     RewriteEngine On
     RewriteBase /
     RewriteRule ^index\.html$ - [L]
     RewriteCond %{REQUEST_FILENAME} !-f
     RewriteCond %{REQUEST_FILENAME} !-d
     RewriteRule . /index.html [L]
   </IfModule>
   ```

---

## ✅ Final Checklist

- [ ] MongoDB Atlas cluster created
- [ ] Database connection string added to backend/.env
- [ ] MONGO_URL, DB_NAME, CORS_ORIGINS configured
- [ ] Backend deployed to Hostinger
- [ ] Dependencies installed (requirements.txt)
- [ ] Database seeded with sample data
- [ ] Backend API tested (all endpoints responding)
- [ ] Frontend built with correct REACT_APP_BACKEND_URL
- [ ] Frontend deployed to Hostinger
- [ ] .htaccess configured for React routing
- [ ] All features tested on production

---

## 📞 Need Help?

**Common Commands:**
```bash
# Check Python version
python --version

# Install dependencies
pip install -r backend/requirements.txt

# Run backend locally
cd backend && uvicorn server:app --reload

# Seed database
python backend/seed_data.py

# Build frontend
cd frontend && yarn build
```

**MongoDB Atlas:**
- Dashboard: https://cloud.mongodb.com
- Free tier: 512MB storage, perfect for starting

**Hostinger Support:**
- Check Hostinger documentation for Python app deployment
- Most Hostinger plans support Python 3.9+

---

## 🎉 You're All Set!

Your CharmTracker backend should now be running on Hostinger with MongoDB Atlas as your database!

**Live API URL:** `https://your-domain.com/api/`

**Test it:** `https://your-domain.com/api/charms`
