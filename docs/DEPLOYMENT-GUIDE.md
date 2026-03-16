# Deployment Guide

## Face Recognition Offline Attendance PWA

---

## 1. Server Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4 cores |
| RAM | 2 GB | 4 GB |
| Storage | 20 GB SSD | 50 GB SSD |
| OS | Ubuntu 20.04 | Ubuntu 22.04 |

---

## 2. Prerequisites

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python 3.10+
sudo apt install -y python3 python3-pip python3-venv

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Install Nginx
sudo apt install -y nginx

# Install Certbot (SSL)
sudo apt install -y certbot python3-certbot-nginx
```

---

## 3. Database Setup

```bash
# Create database and user
sudo -u postgres psql

CREATE DATABASE attendance_db;
CREATE USER attendance_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE attendance_db TO attendance_user;
\q
```

---

## 4. Backend Deployment

```bash
# Clone repository
git clone https://github.com/your-repo/face-attendance.git
cd face-attendance/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
nano .env  # Edit with your values

# Run migrations
alembic upgrade head

# Start with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

---

## 5. Frontend Build

```bash
# PWA App
cd pwa-app
npm install
npm run build  # Output: dist/

# Admin Panel
cd admin-panel
npm install
npm run build  # Output: dist/
```

---

## 6. Nginx Configuration

```nginx
# /etc/nginx/sites-available/attendance

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # PWA App
    location / {
        root /var/www/pwa-app/dist;
        try_files $uri $uri/ /index.html;
    }

    # Admin Panel
    location /admin {
        alias /var/www/admin-panel/dist;
        try_files $uri $uri/ /admin/index.html;
    }

    # API Proxy
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/attendance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 7. SSL Certificate

```bash
sudo certbot --nginx -d your-domain.com
```

---

## 8. Systemd Service

```ini
# /etc/systemd/system/attendance-api.service

[Unit]
Description=Face Attendance API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/backend
Environment="PATH=/var/www/backend/venv/bin"
ExecStart=/var/www/backend/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable attendance-api
sudo systemctl start attendance-api
```

---

## 9. Environment Variables

```env
# .env file
DATABASE_URL=postgresql://attendance_user:password@localhost/attendance_db
SECRET_KEY=your-super-secret-key-change-this
ENCRYPTION_KEY=your-32-byte-encryption-key
CORS_ORIGINS=https://your-domain.com
```

---

## 10. Checklist

- [ ] Server provisioned
- [ ] Domain configured
- [ ] SSL certificate installed
- [ ] Database created
- [ ] Backend deployed
- [ ] Frontend built and deployed
- [ ] Nginx configured
- [ ] Service running
- [ ] Firewall configured (80, 443 open)
- [ ] Backup strategy in place
