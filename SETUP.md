# Setup Guide

## Face Recognition Offline Attendance PWA

---

## Quick Start

### 1. Backend Setup

```bash
cd Face-Recognition-Attendance-PWA/backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Default Admin Login:**
- Username: `admin`
- Password: `admin123`

---

### 2. PWA Frontend Setup

```bash
cd Face-Recognition-Attendance-PWA/pwa-app

# Install dependencies
npm install

# Download face-api models (IMPORTANT!)
cd public/models
# Run the download script from README.md in that folder

# Start dev server
npm run dev
```

**Access:** http://localhost:5173

---

### 3. Download Face-API Models

The face recognition requires pre-trained models. Download them:

```powershell
cd pwa-app/public/models

$baseUrl = "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights"
$models = @(
    "ssd_mobilenetv1_model-weights_manifest.json",
    "ssd_mobilenetv1_model-shard1",
    "ssd_mobilenetv1_model-shard2",
    "face_landmark_68_model-weights_manifest.json",
    "face_landmark_68_model-shard1",
    "face_recognition_model-weights_manifest.json",
    "face_recognition_model-shard1",
    "face_recognition_model-shard2"
)

foreach ($model in $models) {
    Invoke-WebRequest -Uri "$baseUrl/$model" -OutFile $model
    Write-Host "Downloaded: $model"
}
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/login | Login |
| GET | /api/auth/me | Current user |
| GET | /api/employees | List employees |
| POST | /api/employees | Create employee |
| POST | /api/employees/{id}/enroll-face | Enroll face |
| POST | /api/attendance/sync | Sync attendance |
| GET | /api/attendance | List attendance |

---

## Testing Flow

1. **Start Backend** → `uvicorn app.main:app --reload`
2. **Start Frontend** → `npm run dev`
3. **Login** → admin / admin123
4. **Create Employee** via API or admin panel
5. **Enroll Face** for employee
6. **Mark Attendance** using PWA

---

## Project Structure

```
Face-Recognition-Attendance-PWA/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── utils/
│   ├── requirements.txt
│   └── .env
│
├── pwa-app/
│   ├── public/
│   │   └── models/          # Face-api models here
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   └── services/
│   ├── package.json
│   └── vite.config.js
│
└── docs/
```

---

## Troubleshooting

### Camera not working
- Ensure HTTPS or localhost
- Grant camera permission

### Face models not loading
- Check models are in `public/models/`
- Check browser console for errors

### Sync failing
- Check backend is running
- Check network connectivity
- Check browser console

---

## Production Build

```bash
# Backend
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
npm run build
# Deploy dist/ folder to web server
```
