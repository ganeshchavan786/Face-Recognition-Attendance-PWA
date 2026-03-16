# Production Deployment Guide

## 🎯 Overview

This guide covers deploying the Face Recognition Attendance PWA to production using Docker.

---

## 📋 Prerequisites

- Docker & Docker Compose installed
- Domain name configured (e.g., `attendance.yourdomain.com`)
- SSL certificates (Let's Encrypt recommended)
- Server with minimum 2GB RAM, 2 CPU cores

---

## 🚀 Quick Start

### Step 1: Clone and Configure

```bash
# Clone repository
git clone <repository-url>
cd Face-Recognition-Attendance-PWA

# Generate secure keys
cd backend
python generate_keys.py
cd ..

# Create environment file
cp backend/.env.production.example .env
```

### Step 2: Edit .env File

```bash
# Database
DB_USER=attendance
DB_PASSWORD=your-strong-password
DB_NAME=face_attendance

# Security Keys (from generate_keys.py output)
SECRET_KEY=your-generated-secret-key
ENCRYPTION_KEY=your-generated-encryption-key

# Domains
CORS_ORIGINS=https://attendance.yourdomain.com,https://admin.yourdomain.com
```

### Step 3: Setup SSL Certificates

```bash
# Create SSL directory
mkdir -p nginx/ssl

# Option A: Let's Encrypt (recommended)
certbot certonly --standalone -d attendance.yourdomain.com -d admin.yourdomain.com
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/

# Option B: Self-signed (testing only)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/privkey.pem \
  -out nginx/ssl/fullchain.pem
```

### Step 4: Update Nginx Config

Edit `nginx/conf.d/default.conf`:
- Replace `attendance.yourdomain.com` with your actual domain
- Replace `admin.yourdomain.com` with your admin domain

### Step 5: Deploy

```bash
# Linux/Mac
chmod +x scripts/deploy.sh
./scripts/deploy.sh

# Windows
.\scripts\deploy.ps1
```

---

## 🔧 Manual Deployment

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## 📁 Project Structure

```
Face-Recognition-Attendance-PWA/
├── backend/                 # FastAPI Backend
│   ├── Dockerfile
│   ├── .env.production.example
│   └── generate_keys.py
├── pwa-app/                 # PWA Frontend
│   ├── Dockerfile
│   └── nginx.conf
├── admin-panel/             # Admin Dashboard
│   ├── Dockerfile
│   └── nginx.conf
├── nginx/                   # Reverse Proxy
│   ├── nginx.conf
│   ├── conf.d/
│   └── ssl/
├── scripts/
│   ├── deploy.sh
│   ├── deploy.ps1
│   └── backup.sh
├── docker-compose.yml       # Development
└── docker-compose.prod.yml  # Production
```

---

## 🔐 Security Checklist

- [ ] Change default admin password (`admin/admin123`)
- [ ] Generate new SECRET_KEY and ENCRYPTION_KEY
- [ ] Configure HTTPS with valid SSL certificate
- [ ] Set DEBUG=False in production
- [ ] Configure firewall (allow only 80, 443)
- [ ] Setup database backups
- [ ] Configure rate limiting (already in nginx)

---

## 💾 Database Backup

```bash
# Manual backup
./scripts/backup.sh

# Automated backup (cron)
0 2 * * * /path/to/scripts/backup.sh
```

---

## 🔄 Updates

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🐛 Troubleshooting

### Check Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs

# Specific service
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs pwa
```

### Database Connection Issues
```bash
# Check database is running
docker-compose -f docker-compose.prod.yml exec db psql -U attendance -c "SELECT 1"
```

### Restart Services
```bash
docker-compose -f docker-compose.prod.yml restart
```

---

## 📊 Monitoring

### Health Checks
- Backend: `https://attendance.yourdomain.com/api/health`
- PWA: `https://attendance.yourdomain.com/`
- Admin: `https://admin.yourdomain.com/`

### Resource Usage
```bash
docker stats
```

---

## 🌐 DNS Configuration

| Record | Type | Value |
|--------|------|-------|
| attendance | A | your-server-ip |
| admin | A | your-server-ip |

---

## 📱 PWA Installation

After deployment:
1. Open `https://attendance.yourdomain.com` on mobile
2. Click "Add to Home Screen" or install prompt
3. PWA will work offline after first load

---

## ⚠️ Important Notes

1. **ENCRYPTION_KEY**: Backup securely! Losing it = losing all face data
2. **First Login**: Change admin password immediately
3. **Face Models**: Included in build, ~5MB download on first use
4. **Offline Mode**: Requires initial online sync for employee data
