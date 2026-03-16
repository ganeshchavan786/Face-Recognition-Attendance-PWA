#!/bin/bash
# ===========================================
# Database Backup Script
# ===========================================

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/face_attendance_$TIMESTAMP.sql"

# Create backup directory if not exists
mkdir -p $BACKUP_DIR

echo "Creating database backup..."

# Backup PostgreSQL database
docker-compose exec -T db pg_dump -U ${DB_USER:-attendance} ${DB_NAME:-face_attendance} > $BACKUP_FILE

# Compress backup
gzip $BACKUP_FILE

echo "Backup created: ${BACKUP_FILE}.gz"

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "Old backups cleaned up."
