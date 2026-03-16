# 🚀 Easy Install - 5 Minute Deployment

Deploy Face Recognition Attendance PWA in production with just one command!

## 📋 Prerequisites

- Ubuntu/Debian based VPS or server
- SSH access with sudo privileges
- Domain name (optional but recommended)

## 🎯 One-Command Installation

### Method 1: Direct Download & Run
```bash
# Download and run the script
curl -fsSL https://raw.githubusercontent.com/ganeshchavan786/Face-Recognition-Attendance-PWA/main/easy-install.sh | bash -s -- attendance_prod yourdomain.com admin@yourdomain.com
```

### Method 2: Download & Execute
```bash
# Download the script
wget https://raw.githubusercontent.com/ganeshchavan786/Face-Recognition-Attendance-PWA/main/easy-install.sh

# Make executable
chmod +x easy-install.sh

# Run installation
./easy-install.sh attendance_prod yourdomain.com admin@yourdomain.com
```

## 📝 Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `attendance_prod` | Project directory name | Where the app will be installed |
| `yourdomain.com` | Domain name | Your domain for the app |
| `admin@yourdomain.com` | Email | Admin email (not used currently) |

## 🌟 Features

✅ **Automatic Docker Installation** - Installs Docker & Docker Compose  
✅ **Git Clone** - Downloads latest code from GitHub  
✅ **Secret Key Generation** - Generates secure SECRET_KEY and ENCRYPTION_KEY  
✅ **Environment Setup** - Configures production environment  
✅ **Docker Compose Deployment** - Starts all services automatically  
✅ **Health Checks** - Verifies deployment success  
✅ **5 Minute Deployment** - Complete setup in 5 minutes  

## 🌐 Access URLs

After installation, your app will be available at:

| Service | URL |
|---------|-----|
| 📱 Main App | `http://yourdomain.com` |
| ⚙️ Admin Panel | `http://yourdomain.com:3000` |
| 📚 API Docs | `http://yourdomain.com:8000/docs` |

## 🔧 Management Commands

After installation, navigate to project directory:
```bash
cd ~/attendance_prod
```

### Common Commands:
```bash
# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Update to latest version
git pull
docker-compose build --no-cache
docker-compose up -d
```

## 🛠️ Troubleshooting

### If deployment fails:
```bash
# Check logs
cd ~/attendance_prod
docker-compose logs

# Restart services
docker-compose restart

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Port conflicts:
```bash
# Check what's using ports
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :8000
```

## 🔒 Security Notes

- Default keys are generated automatically
- Change default admin password after first login
- Configure firewall to allow only necessary ports
- Set up SSL certificate for production use

## 📱 Mobile Access

The PWA works best with HTTPS. For production:
1. Set up domain DNS
2. Configure SSL certificate (Let's Encrypt)
3. Access via HTTPS on mobile devices

## 🆘 Support

If you face any issues:
1. Check the logs: `docker-compose logs`
2. Verify Docker is running: `systemctl status docker`
3. Check ports: `netstat -tulpn | grep -E ':(80|3000|8000)'`

---

**🎉 That's it! Your Face Recognition Attendance PWA is running in production!**
