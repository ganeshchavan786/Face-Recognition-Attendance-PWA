# 🛠️ Technology Stack Documentation

## Face Recognition Offline Attendance PWA

**Requirement: 100% Open Source - MIT License Compatible**

---

## 📱 Frontend PWA (Employee App)

### Core Framework

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| react | ^18.2.0 | MIT | UI Framework |
| react-dom | ^18.2.0 | MIT | React DOM rendering |
| react-router-dom | ^6.x | MIT | Client-side routing |

### Build Tools

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| vite | ^5.x | MIT | Build tool & dev server |
| @vitejs/plugin-react | ^4.x | MIT | React plugin for Vite |
| vite-plugin-pwa | ^0.17.x | MIT | PWA support for Vite |

### Styling

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| tailwindcss | ^3.x | MIT | Utility-first CSS |
| postcss | ^8.x | MIT | CSS processing |
| autoprefixer | ^10.x | MIT | CSS vendor prefixes |
| @headlessui/react | ^1.x | MIT | Accessible UI components |
| lucide-react | ^0.x | ISC | Icon library |

### Face Recognition

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| face-api.js | ^0.22.2 | MIT | Face detection & recognition |
| @tensorflow/tfjs | ^4.x | Apache 2.0 | ML runtime (face-api dependency) |

### Offline Storage

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| idb | ^7.x | ISC | IndexedDB wrapper |

### PWA & Service Worker

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| workbox-core | ^7.x | MIT | Service worker toolkit |
| workbox-precaching | ^7.x | MIT | Precaching strategies |
| workbox-routing | ^7.x | MIT | Request routing |
| workbox-strategies | ^7.x | MIT | Caching strategies |
| workbox-background-sync | ^7.x | MIT | Background sync |

### HTTP Client

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| axios | ^1.x | MIT | HTTP requests |

### Utilities

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| date-fns | ^2.x | MIT | Date manipulation |
| uuid | ^9.x | MIT | UUID generation |
| compressorjs | ^1.x | MIT | Image compression |

---

## 🖥️ Admin Panel (React Web App)

### Core (Same as PWA)
- react, react-dom, react-router-dom

### UI Components

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| @headlessui/react | ^1.x | MIT | Accessible components |
| @heroicons/react | ^2.x | MIT | Icon set |
| tailwindcss | ^3.x | MIT | Styling |

### Data Visualization

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| recharts | ^2.x | MIT | Charts & graphs |

### Data Export

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| xlsx | ^0.18.x | Apache 2.0 | Excel export |
| jspdf | ^2.x | MIT | PDF generation |
| jspdf-autotable | ^3.x | MIT | PDF tables |

### Tables & Forms

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| @tanstack/react-table | ^8.x | MIT | Data tables |
| react-hook-form | ^7.x | MIT | Form handling |
| zod | ^3.x | MIT | Schema validation |

---

## ⚙️ Backend (FastAPI)

### Core Framework

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| fastapi | ^0.104.x | MIT | Web framework |
| uvicorn | ^0.24.x | BSD | ASGI server |
| python-multipart | ^0.0.6 | Apache 2.0 | Form data parsing |

### Database

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| sqlalchemy | ^2.x | MIT | ORM |
| alembic | ^1.x | MIT | DB migrations |
| aiosqlite | ^0.19.x | MIT | Async SQLite |
| asyncpg | ^0.29.x | Apache 2.0 | Async PostgreSQL |

### Authentication

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| python-jose[cryptography] | ^3.x | MIT | JWT handling |
| passlib[bcrypt] | ^1.x | BSD | Password hashing |
| bcrypt | ^4.x | Apache 2.0 | Bcrypt algorithm |

### Security & Encryption

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| cryptography | ^41.x | Apache 2.0/BSD | AES encryption |

### Validation

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| pydantic | ^2.x | MIT | Data validation |
| email-validator | ^2.x | CC0 | Email validation |

### Reports

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| openpyxl | ^3.x | MIT | Excel generation |
| reportlab | ^4.x | BSD | PDF generation |

### Utilities

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| python-dotenv | ^1.x | BSD | Environment variables |
| httpx | ^0.25.x | BSD | HTTP client |

---

## 🗄️ Database Options

### Development
| Database | License | Notes |
|----------|---------|-------|
| SQLite | Public Domain | Zero config, file-based |

### Production
| Database | License | Notes |
|----------|---------|-------|
| PostgreSQL | PostgreSQL License | Recommended for production |
| MySQL | GPL | Alternative option |

---

## 🔧 Development Tools

### Code Quality

| Tool | License | Purpose |
|------|---------|---------|
| ESLint | MIT | JavaScript linting |
| Prettier | MIT | Code formatting |
| Black | MIT | Python formatting |
| Ruff | MIT | Python linting |
| mypy | MIT | Python type checking |

### Testing

| Tool | License | Purpose |
|------|---------|---------|
| pytest | MIT | Python testing |
| pytest-asyncio | Apache 2.0 | Async test support |
| vitest | MIT | JavaScript testing |
| @testing-library/react | MIT | React testing |

---

## 🌐 Deployment

### Server

| Tool | License | Purpose |
|------|---------|---------|
| Nginx | BSD | Reverse proxy |
| Gunicorn | MIT | Python WSGI server |
| Docker | Apache 2.0 | Containerization |

### SSL

| Tool | License | Purpose |
|------|---------|---------|
| Let's Encrypt | Free | SSL certificates |
| Certbot | Apache 2.0 | Certificate automation |

---

## 📦 Package.json (PWA)

```json
{
  "name": "face-attendance-pwa",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "face-api.js": "^0.22.2",
    "idb": "^7.1.1",
    "axios": "^1.6.0",
    "date-fns": "^2.30.0",
    "uuid": "^9.0.0",
    "compressorjs": "^1.2.1",
    "lucide-react": "^0.294.0",
    "@headlessui/react": "^1.7.17"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "vite-plugin-pwa": "^0.17.0",
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "workbox-core": "^7.0.0",
    "workbox-precaching": "^7.0.0",
    "workbox-routing": "^7.0.0",
    "workbox-strategies": "^7.0.0",
    "workbox-background-sync": "^7.0.0"
  }
}
```

---

## 📦 requirements.txt (Backend)

```txt
# Core
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.23
alembic==1.12.1
aiosqlite==0.19.0

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.1

# Validation
pydantic==2.5.2
email-validator==2.1.0

# Security
cryptography==41.0.7

# Reports
openpyxl==3.1.2
reportlab==4.0.7

# Utilities
python-dotenv==1.0.0
httpx==0.25.2

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
ruff==0.1.6
```

---

## 🔒 License Compliance Summary

| Category | Licenses Used | Compliant |
|----------|---------------|-----------|
| Frontend | MIT, ISC, Apache 2.0 | ✅ Yes |
| Backend | MIT, BSD, Apache 2.0 | ✅ Yes |
| Database | Public Domain, PostgreSQL | ✅ Yes |
| Tools | MIT, BSD, Apache 2.0 | ✅ Yes |

**All packages are open source and compatible with commercial use.**

---

## 📝 Notes

1. **face-api.js** is the core face recognition library (MIT license)
2. **TensorFlow.js** is required by face-api.js (Apache 2.0)
3. All UI components use MIT-licensed libraries
4. No paid/proprietary dependencies required
5. System can be deployed on any Linux server
