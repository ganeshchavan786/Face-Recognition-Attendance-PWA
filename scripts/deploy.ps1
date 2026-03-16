# ===========================================
# Production Deployment Script (Windows)
# ===========================================

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Face Attendance - Production Deployment" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env file not found!" -ForegroundColor Red
    Write-Host "Copy .env.example to .env and configure it first."
    exit 1
}

Write-Host ""
Write-Host "Step 1: Building Docker images..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml build

Write-Host ""
Write-Host "Step 2: Starting services..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml up -d

Write-Host ""
Write-Host "Step 3: Waiting for database..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Services:"
Write-Host "  - PWA:    https://attendance.yourdomain.com"
Write-Host "  - Admin:  https://admin.yourdomain.com"
Write-Host "  - API:    https://attendance.yourdomain.com/api"
Write-Host ""
Write-Host "Default Admin: admin / admin123" -ForegroundColor Yellow
Write-Host "CHANGE THIS PASSWORD IMMEDIATELY!" -ForegroundColor Red
Write-Host ""
