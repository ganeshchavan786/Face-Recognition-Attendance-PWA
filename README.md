# Face Recognition Based Offline Attendance PWA

## 🎯 Project Overview

A **Progressive Web App (PWA)** for face recognition-based employee attendance that works **offline-first**. Designed for remote areas with low/no internet connectivity.

---

## 📋 Key Features

- **Offline-First Architecture** - Works without internet
- **Face Recognition** - Secure biometric attendance
- **Auto Background Sync** - Syncs when online
- **PWA Installable** - Install on mobile/desktop
- **Admin Dashboard** - Complete management panel
- **GPS Location Capture** - Location-based verification
- **Liveness Detection** - Anti-spoofing protection

---

## 🛠️ Technology Stack (100% MIT Open Source)

### Frontend (PWA)
| Technology | Purpose | License |
|------------|---------|---------|
| React 18 | UI Framework | MIT |
| Vite | Build Tool | MIT |
| TailwindCSS | Styling | MIT |
| face-api.js | Face Recognition | MIT |
| idb | IndexedDB Wrapper | ISC |
| Workbox | Service Worker | MIT |

### Backend
| Technology | Purpose | License |
|------------|---------|---------|
| FastAPI | REST API | MIT |
| SQLAlchemy | ORM | MIT |
| SQLite/PostgreSQL | Database | Public Domain/PostgreSQL |
| python-jose | JWT Auth | MIT |
| cryptography | Encryption | Apache 2.0/BSD |

### Admin Panel
| Technology | Purpose | License |
|------------|---------|---------|
| React 18 | UI Framework | MIT |
| React Router | Navigation | MIT |
| Axios | HTTP Client | MIT |
| Recharts | Charts | MIT |
| jsPDF | PDF Export | MIT |
| xlsx | Excel Export | Apache 2.0 |

---

## 📁 Project Structure

```
Face-Recognition-Attendance-PWA/
├── docs/                          # Documentation
│   ├── SRS.md                     # Software Requirements
│   ├── ARCHITECTURE.md            # System Architecture
│   ├── API-DOCUMENTATION.md       # API Specs
│   ├── DEPLOYMENT-GUIDE.md        # Deployment Instructions
│   └── SECURITY.md                # Security Guidelines
│
├── backend/                       # FastAPI Backend
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   ├── alembic/                   # DB Migrations
│   ├── tests/
│   └── requirements.txt
│
├── pwa-app/                       # Employee PWA
│   ├── public/
│   │   ├── manifest.json
│   │   └── models/                # Face-api models
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── db/                    # IndexedDB
│   └── package.json
│
├── admin-panel/                   # Admin React App
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
│
├── TODO.md                        # Phase-wise TODO
├── TECH-STACK.md                  # Technology Details
└── README.md                      # This file
```

---

## 🚀 Quick Start

### 🎯 Option 1: One-Command Production Deployment (Recommended)

Deploy in **5 minutes** with automated setup:

```bash
# Method A: Direct download & run
curl -fsSL https://raw.githubusercontent.com/ganeshchavan786/Face-Recognition-Attendance-PWA/main/easy-install.sh | bash -s -- attendance_prod yourdomain.com admin@yourdomain.com

# Method B: Download & execute
wget https://raw.githubusercontent.com/ganeshchavan786/Face-Recognition-Attendance-PWA/main/easy-install.sh
chmod +x easy-install.sh
./easy-install.sh attendance_prod yourdomain.com admin@yourdomain.com
```

**✅ Features:**
- Auto Docker installation
- Secure key generation
- Production-ready setup
- SSL ready
- Health checks included

### 🛠️ Option 2: Manual Development Setup

#### Prerequisites
- Node.js 18+
- Python 3.10+
- Modern Browser (Chrome/Edge)

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### PWA Setup
```bash
cd pwa-app
npm install
npm run dev
```

#### Admin Panel Setup
```bash
cd admin-panel
npm install
npm run dev
```

### 🐳 Option 3: Docker Development

```bash
# Clone and run
git clone https://github.com/ganeshchavan786/Face-Recognition-Attendance-PWA.git
cd Face-Recognition-Attendance-PWA
docker-compose up -d

# Access URLs:
# PWA: http://localhost:80
# Admin: http://localhost:3000
# API: http://localhost:8000/docs
```

---

## 🌐 Production Deployment

### 🎯 Easy Production Setup

```bash
# One-command production deployment
curl -fsSL https://raw.githubusercontent.com/ganeshchavan786/Face-Recognition-Attendance-PWA/main/easy-install.sh | bash -s -- production yourdomain.com admin@yourdomain.com
```

### 📋 Production URLs

| Service | URL | Description |
|---------|-----|-------------|
| 📱 PWA App | `https://yourdomain.com` | Employee attendance app |
| ⚙️ Admin Panel | `https://yourdomain.com:3000` | Management dashboard |
| 📚 API Docs | `https://yourdomain.com:8000/docs` | API documentation |

### 🔧 VPS Deployment

```bash
# On any Ubuntu/Debian VPS
git clone https://github.com/ganeshchavan786/Face-Recognition-Attendance-PWA.git
cd Face-Recognition-Attendance-PWA
./easy-install.sh attendance_prod yourdomain.com admin@yourdomain.com
```

### 🐳 Docker Images

Pre-built Docker images available:
- `ganeshchavan963/face-attendance-backend:latest`
- `ganeshchavan963/face-attendance-pwa:latest`
- `ganeshchavan963/face-attendance-admin:latest`

### 📱 PWA Installation

1. Open PWA URL in Chrome/Edge
2. Click "Install" prompt or menu → "Install App"
3. App icon appears on home screen
4. Works offline after first load

---

## 🔐 Security Features

- JWT Token Authentication
- Role-Based Access Control (RBAC)
- AES-256 Face Descriptor Encryption
- Device Binding (UUID)
- HTTPS Mandatory
- Attendance Time Window Lock

---

## 📊 User Roles

| Role | Permissions |
|------|-------------|
| Employee | Mark attendance, View own history |
| Supervisor | View team attendance, Reports |
| Admin | Full access, Employee management, Face enrollment |

---

## 📄 License

MIT License - 100% Open Source

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

## 📞 Support

For issues and feature requests, please create a GitHub issue.
