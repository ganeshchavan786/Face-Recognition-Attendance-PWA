# Software Requirements Specification (SRS)

## Face Recognition Based Offline Attendance – Progressive Web App (PWA)

**Version:** 1.0  
**Date:** December 2024  
**Status:** Production Ready

---

## 1. Introduction

### 1.1 Purpose

This document defines the complete software requirements for a **Face Recognition based Offline Attendance Progressive Web App (PWA)**. The system records employee attendance in both online and offline environments, specifically designed for remote or low-connectivity areas.

### 1.2 Scope

The system provides:
- Face recognition–based attendance marking
- Offline-first PWA architecture
- Automatic background synchronization
- Admin web dashboard for monitoring and reporting
- Secure face data storage with encryption

### 1.3 Definitions & Acronyms

| Term | Definition |
|------|------------|
| PWA | Progressive Web App |
| IndexedDB | Browser-based local database |
| Face Descriptor | 128-dimensional numerical vector representing facial features |
| Sync Queue | Pending offline data waiting for server upload |
| JWT | JSON Web Token for authentication |
| RBAC | Role-Based Access Control |

---

## 2. Overall Description

### 2.1 Product Perspective

```
┌─────────────────────────────────────────────────────────────────┐
│                    System Architecture                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Employee    │    │   Backend    │    │    Admin     │      │
│  │   PWA App    │◄──►│   REST API   │◄──►│    Panel     │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                   │                                   │
│         ▼                   ▼                                   │
│  ┌──────────────┐    ┌──────────────┐                          │
│  │  IndexedDB   │    │  PostgreSQL  │                          │
│  │  (Offline)   │    │  (Server)    │                          │
│  └──────────────┘    └──────────────┘                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 User Classes

| User | Description | Access Level |
|------|-------------|--------------|
| Employee | Marks attendance using face recognition | Own data only |
| Supervisor | Reviews team attendance data | Team data |
| Admin | Manages employees, views reports, enrolls faces | Full access |

### 2.3 Operating Environment

| Component | Requirement |
|-----------|-------------|
| Browser | Chrome 80+, Edge 80+ (Android/Desktop) |
| OS | Android 8+, Windows 10+, Linux |
| Server | Linux VPS / Cloud (Ubuntu 20.04+) |
| Camera | Front-facing camera (min 720p) |
| Storage | 100MB local storage for PWA |

---

## 3. Functional Requirements

### 3.1 User Authentication

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | System shall authenticate users using JWT tokens | High |
| FR-02 | System shall allow offline access for attendance once authenticated | High |
| FR-03 | System shall auto-refresh tokens before expiry | Medium |
| FR-04 | System shall logout user on token expiry | High |

### 3.2 Face Enrollment

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-05 | Admin shall enroll employee face data | High |
| FR-06 | System shall capture 5-10 face angles during enrollment | High |
| FR-07 | System shall generate average face descriptor | High |
| FR-08 | System shall store encrypted face descriptors | High |
| FR-09 | System shall validate face quality before enrollment | Medium |

### 3.3 Attendance Capture (Offline)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-10 | System shall capture attendance without internet | High |
| FR-11 | System shall store attendance in IndexedDB | High |
| FR-12 | System shall tag records as PENDING_SYNC | High |
| FR-13 | System shall capture GPS coordinates | Medium |
| FR-14 | System shall capture face snapshot | Medium |
| FR-15 | System shall capture timestamp | High |

### 3.4 Face Recognition

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-16 | System shall compare live face with stored descriptor | High |
| FR-17 | System shall use Euclidean distance for matching | High |
| FR-18 | System shall reject mismatched faces (threshold > 0.6) | High |
| FR-19 | System shall complete recognition in < 3 seconds | High |

### 3.5 Liveness Detection

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-20 | System shall detect eye blinks | Medium |
| FR-21 | System shall prompt random actions | Medium |
| FR-22 | System shall reject photo/video spoofing | Medium |

### 3.6 Data Synchronization

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-23 | System shall auto-sync pending records when online | High |
| FR-24 | System shall prevent duplicate attendance | High |
| FR-25 | System shall handle partial sync failures | High |
| FR-26 | System shall retry failed syncs | Medium |

### 3.7 Admin Functions

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-27 | Admin shall manage employee records | High |
| FR-28 | Admin shall view attendance reports | High |
| FR-29 | Admin shall export reports (Excel/PDF) | Medium |
| FR-30 | Admin shall approve/reject attendance | Medium |

---

## 4. Non-Functional Requirements

### 4.1 Performance

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | Face recognition time | < 3 seconds |
| NFR-02 | App load time (cached) | < 2 seconds |
| NFR-03 | Sync batch size | 50 records max |
| NFR-04 | IndexedDB query time | < 100ms |

### 4.2 Security

| ID | Requirement |
|----|-------------|
| NFR-05 | HTTPS mandatory for all communications |
| NFR-06 | Face descriptors encrypted with AES-256 |
| NFR-07 | JWT tokens with 1-hour expiry |
| NFR-08 | Role-based access control (RBAC) |
| NFR-09 | Device binding using UUID |
| NFR-10 | Password hashing with bcrypt |

### 4.3 Reliability

| ID | Requirement |
|----|-------------|
| NFR-11 | Offline data must persist until synced |
| NFR-12 | No data loss on browser refresh |
| NFR-13 | Graceful degradation on network failure |
| NFR-14 | 99.9% uptime for backend services |

### 4.4 Usability

| ID | Requirement |
|----|-------------|
| NFR-15 | Single-click attendance marking |
| NFR-16 | Clear visual feedback for all actions |
| NFR-17 | Offline status indicator |
| NFR-18 | Mobile-first responsive design |

---

## 5. Data Models

### 5.1 Employee

```
Employee {
  id: UUID (PK)
  emp_code: String (Unique)
  name: String
  email: String
  department: String
  face_descriptor: Encrypted<Float[128]>
  status: Enum (ACTIVE, INACTIVE)
  created_at: DateTime
  updated_at: DateTime
}
```

### 5.2 Attendance

```
Attendance {
  id: UUID (PK)
  emp_id: UUID (FK → Employee)
  date: Date
  time: Time
  latitude: Float
  longitude: Float
  device_id: String
  photo: Base64 (compressed)
  sync_status: Enum (PENDING, SYNCED, FAILED)
  created_at: DateTime
  synced_at: DateTime (nullable)
}
```

### 5.3 User (Authentication)

```
User {
  id: UUID (PK)
  username: String (Unique)
  password_hash: String
  role: Enum (ADMIN, SUPERVISOR, EMPLOYEE)
  emp_id: UUID (FK → Employee, nullable)
  is_active: Boolean
  created_at: DateTime
}
```

---

## 6. API Specifications

### 6.1 Authentication

#### POST /api/auth/login
```json
Request:
{
  "username": "string",
  "password": "string"
}

Response (200):
{
  "access_token": "jwt-token",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid",
    "username": "string",
    "role": "EMPLOYEE|SUPERVISOR|ADMIN"
  }
}
```

### 6.2 Employees

#### GET /api/employees
```json
Headers: Authorization: Bearer <token>

Response (200):
{
  "employees": [
    {
      "id": "uuid",
      "emp_code": "EMP001",
      "name": "John Doe",
      "department": "IT",
      "face_descriptor": [0.12, -0.45, ...] // 128 floats
    }
  ]
}
```

#### POST /api/employees
```json
Headers: Authorization: Bearer <token> (Admin only)

Request:
{
  "emp_code": "EMP001",
  "name": "John Doe",
  "email": "john@example.com",
  "department": "IT"
}

Response (201):
{
  "id": "uuid",
  "emp_code": "EMP001",
  "name": "John Doe"
}
```

### 6.3 Face Enrollment

#### POST /api/employees/{id}/enroll-face
```json
Headers: Authorization: Bearer <token> (Admin only)

Request:
{
  "face_descriptors": [
    [0.12, -0.45, ...], // 128 floats each
    [0.13, -0.44, ...],
    // 5-10 samples
  ]
}

Response (200):
{
  "status": "success",
  "message": "Face enrolled successfully"
}
```

### 6.4 Attendance Sync

#### POST /api/attendance/sync
```json
Headers: Authorization: Bearer <token>

Request:
{
  "device_id": "DEV-UUID",
  "records": [
    {
      "local_id": "local-uuid",
      "emp_id": "uuid",
      "date": "2025-01-01",
      "time": "09:15:00",
      "latitude": 18.5204,
      "longitude": 73.8567,
      "photo": "base64-compressed-image"
    }
  ]
}

Response (200):
{
  "status": "success",
  "synced": 1,
  "failed": 0,
  "results": [
    {
      "local_id": "local-uuid",
      "server_id": "uuid",
      "status": "synced"
    }
  ]
}
```

### 6.5 Reports

#### GET /api/reports/attendance
```json
Headers: Authorization: Bearer <token>

Query Params:
- start_date: YYYY-MM-DD
- end_date: YYYY-MM-DD
- emp_id: uuid (optional)
- department: string (optional)

Response (200):
{
  "records": [...],
  "summary": {
    "total_present": 25,
    "total_absent": 5,
    "total_employees": 30
  }
}
```

---

## 7. User Interface Specifications

### 7.1 PWA Screens

| Screen | Components |
|--------|------------|
| Login | Username, Password, Login Button, Offline Badge |
| Attendance | Camera Preview, Employee Name, Mark Button, Status |
| History | Date Filter, Attendance List, Sync Status |
| Profile | Employee Info, Logout Button |

### 7.2 Admin Panel Screens

| Screen | Components |
|--------|------------|
| Dashboard | Stats Cards, Charts, Recent Activity |
| Employees | List, Add/Edit Forms, Face Enrollment |
| Attendance | Table, Filters, Approve/Reject |
| Reports | Date Range, Export Buttons, Charts |
| Settings | System Config, User Management |

---

## 8. Constraints & Assumptions

### 8.1 Constraints

1. Device must have front-facing camera
2. HTTPS required for camera access
3. Browser must support Service Workers
4. Minimum 100MB local storage available

### 8.2 Assumptions

1. Users will grant camera permission
2. Users will grant location permission
3. Adequate lighting for face detection
4. Single face per attendance capture

---

## 9. Acceptance Criteria

### 9.1 Face Recognition
- [ ] Detects face within 2 seconds
- [ ] Matches correct employee with 95%+ accuracy
- [ ] Rejects unknown faces
- [ ] Works in varied lighting conditions

### 9.2 Offline Mode
- [ ] Marks attendance without internet
- [ ] Stores data locally
- [ ] Syncs automatically when online
- [ ] No data loss on app restart

### 9.3 Admin Panel
- [ ] Manages employees
- [ ] Views all attendance
- [ ] Exports reports
- [ ] Enrolls faces

---

## 10. Appendix

### 10.1 Face-api.js Models Required

| Model | Size | Purpose |
|-------|------|---------|
| ssd_mobilenetv1 | 5.4 MB | Face detection |
| face_landmark_68 | 350 KB | Facial landmarks |
| face_recognition | 6.2 MB | Face descriptor |

### 10.2 IndexedDB Schema

```javascript
// Database: attendance-db
// Version: 1

// Object Stores:
1. employees (keyPath: id)
   - Indexes: emp_code (unique)

2. attendance (keyPath: id)
   - Indexes: emp_id, date, sync_status

3. sync_queue (keyPath: id)
   - Indexes: status, created_at
```

---

**Document Status:** ✅ Complete  
**Last Updated:** December 2024
