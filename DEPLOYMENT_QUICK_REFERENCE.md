# 🎯 Quick Deployment Reference for CharmTracker

## 📍 Entry Points & Commands

### **Main Entry File:**
```
backend/server.py
```

### **Start Commands (Choose One):**

**1. Uvicorn (Development/Simple Hosting):**
```bash
uvicorn backend.server:app --host 0.0.0.0 --port 8000
```

**2. Gunicorn (Production - Recommended):**
```bash
gunicorn backend.server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**3. Using Startup Script:**
```bash
./start.sh
```

**4. Passenger WSGI (Some shared hosting):**
```
Entry Point: passenger_wsgi.py
```

---

## 🔧 Required Environment Variables

### **Backend (.env location: `backend/.env`)**
```env
MONGO_URL="mongodb://localhost:27017"  # Or MongoDB Atlas URL
DB_NAME="charmtracker_production"
CORS_ORIGINS="*"  # Or specific domains separated by commas
```

### **Frontend (.env location: `frontend/.env`)**
```env
REACT_APP_BACKEND_URL=https://your-api-domain.com
```

---

## 🗄️ Database Setup

### **1. MongoDB Atlas (Recommended for Production)**
- Sign up: https://www.mongodb.com/cloud/atlas
- Create free cluster (512MB)
- Get connection string
- Whitelist IP: 0.0.0.0/0 (all IPs) in Network Access

### **2. Seed Database:**
```bash
python backend/seed_data.py
```

---

## 📦 Dependencies Installation

```bash
# Backend
pip install -r backend/requirements.txt

# Frontend
cd frontend
yarn install
```

---

## 🏗️ Frontend Build for Production

```bash
cd frontend
yarn build
# Upload the 'build/' folder to your web server
```

---

## 🧪 Test Your Deployment

```bash
# Test root endpoint
curl https://your-domain.com/api/

# Test charms endpoint
curl https://your-domain.com/api/charms?page=1&limit=5

# Test trending
curl https://your-domain.com/api/trending
```

---

## 📂 File Structure for Hosting

```
your-website/
├── passenger_wsgi.py       ← WSGI entry point (if using Passenger)
├── start.sh               ← Startup script
├── backend/
│   ├── server.py         ← Main application
│   ├── .env              ← Backend config (INCLUDED in git)
│   ├── requirements.txt  ← Python dependencies
│   ├── models/
│   ├── routes/
│   └── seed_data.py
└── frontend/
    ├── .env              ← Frontend config (INCLUDED in git)
    ├── build/            ← Production build (after yarn build)
    └── package.json
```

---

## 🚀 Hostinger Specific Settings

### **In Hostinger Control Panel:**

1. **Select:** Python App
2. **Python Version:** 3.9+
3. **Application Root:** `/home/username/htdocs`
4. **Application URL:** Your domain
5. **Application Startup File:** `backend/server.py`
6. **Application Entry Point:** `app`
7. **Environment Variables:** Add MONGO_URL, DB_NAME, CORS_ORIGINS

### **Or Use This Command:**
```bash
uvicorn backend.server:app --host 0.0.0.0 --port 8000
```

---

## ✅ Deployment Checklist

- [ ] MongoDB Atlas cluster ready
- [ ] Updated backend/.env with MongoDB URL
- [ ] Updated frontend/.env with backend URL
- [ ] Installed backend dependencies
- [ ] Seeded database
- [ ] Built frontend (yarn build)
- [ ] Uploaded to Hostinger
- [ ] Configured start command
- [ ] Tested all API endpoints
- [ ] Verified frontend connects to backend

---

## 🎉 You're Ready!

**API Base URL:** `https://your-domain.com/api`

**Available Endpoints:**
- GET /api/ - Health check
- GET /api/charms - All charms (with filters)
- GET /api/charms/:id - Specific charm
- GET /api/trending - Top 6 trending
- GET /api/market-overview - Market stats

**Full Documentation:** See `HOSTINGER_DEPLOYMENT.md`
