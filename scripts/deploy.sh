#!/bin/bash
# ===========================================
# Production Deployment Script
# ===========================================

set -e

echo "=========================================="
echo "Face Attendance - Production Deployment"
echo "=========================================="

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Copy .env.example to .env and configure it first."
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check required variables
if [ -z "$SECRET_KEY" ] || [ -z "$ENCRYPTION_KEY" ]; then
    echo "ERROR: SECRET_KEY and ENCRYPTION_KEY must be set in .env"
    exit 1
fi

echo ""
echo "Step 1: Building Docker images..."
docker-compose -f docker-compose.prod.yml build

echo ""
echo "Step 2: Starting services..."
docker-compose -f docker-compose.prod.yml up -d

echo ""
echo "Step 3: Waiting for database..."
sleep 10

echo ""
echo "Step 4: Running database migrations..."
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Services:"
echo "  - PWA:    https://attendance.yourdomain.com"
echo "  - Admin:  https://admin.yourdomain.com"
echo "  - API:    https://attendance.yourdomain.com/api"
echo ""
echo "Default Admin: admin / admin123"
echo "CHANGE THIS PASSWORD IMMEDIATELY!"
echo ""
