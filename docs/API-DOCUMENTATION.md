# API Documentation

## Face Recognition Offline Attendance PWA

**Base URL:** `https://your-domain.com/api`  
**Authentication:** JWT Bearer Token

---

## 1. Authentication

### POST /api/auth/login
```json
Request:
{ "username": "string", "password": "string" }

Response (200):
{
  "access_token": "jwt-token",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": { "id": "uuid", "username": "string", "role": "EMPLOYEE|SUPERVISOR|ADMIN" }
}
```

### POST /api/auth/refresh
Refresh expired token. Returns new access_token.

### GET /api/auth/me
Get current user details.

---

## 2. Employees

### GET /api/employees
List all employees with face descriptors (for offline cache).

Query: `?page=1&limit=50&department=IT&status=ACTIVE`

### GET /api/employees/{id}
Get single employee.

### POST /api/employees (Admin)
```json
Request:
{ "emp_code": "EMP001", "name": "John Doe", "email": "john@example.com", "department": "IT" }
```

### PUT /api/employees/{id} (Admin)
Update employee details.

### DELETE /api/employees/{id} (Admin)
Soft delete (deactivate) employee.

---

## 3. Face Enrollment

### POST /api/employees/{id}/enroll-face (Admin)
```json
Request:
{
  "face_descriptors": [
    [0.12, -0.45, ...],  // 128 floats - 5-10 samples required
  ]
}

Response:
{ "status": "success", "message": "Face enrolled successfully" }
```

### GET /api/employees/{id}/face-status
Check enrollment status.

### DELETE /api/employees/{id}/face (Admin)
Remove face data.

---

## 4. Attendance

### POST /api/attendance/sync
```json
Request:
{
  "device_id": "DEV-UUID",
  "records": [
    {
      "local_id": "uuid",
      "emp_id": "uuid",
      "date": "2025-01-01",
      "time": "09:15:30",
      "latitude": 18.5204,
      "longitude": 73.8567,
      "photo": "base64-compressed"
    }
  ]
}

Response:
{
  "status": "success",
  "synced": 1,
  "failed": 0,
  "results": [{ "local_id": "uuid", "server_id": "uuid", "status": "synced" }]
}
```

### GET /api/attendance
Query: `?start_date=2025-01-01&end_date=2025-01-31&emp_id=uuid&department=IT`

---

## 5. Reports

### GET /api/reports/attendance
Get attendance report with summary.

### GET /api/reports/export/excel
Download Excel report.

### GET /api/reports/export/pdf
Download PDF report.

---

## 6. Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict (Duplicate) |
| 500 | Server Error |
