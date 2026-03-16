# Production-Ready SRS

## Face Recognition Offline Attendance PWA

---

## 1. System Overview

| Aspect | Description |
|--------|-------------|
| **Purpose** | Offline-first face attendance for remote areas |
| **Users** | Employee, Supervisor, Admin |
| **Platform** | PWA (Chrome/Edge), FastAPI Backend |
| **License** | 100% MIT Open Source |

---

## 2. Functional Requirements

### Authentication (FR-01 to FR-04)
- JWT token authentication
- Offline access after login
- Auto token refresh
- Role-based access

### Face Enrollment (FR-05 to FR-09)
- Admin enrolls employee faces
- 5-10 face samples required
- Average descriptor generated
- AES-256 encrypted storage

### Attendance (FR-10 to FR-15)
- Works without internet
- Stores in IndexedDB
- Captures GPS, timestamp, photo
- Tags as PENDING_SYNC

### Face Recognition (FR-16 to FR-19)
- Euclidean distance matching
- Threshold: 0.6
- Recognition < 3 seconds

### Liveness (FR-20 to FR-22)
- Eye blink detection
- Random prompts
- Anti-spoofing

### Sync (FR-23 to FR-26)
- Auto-sync when online
- Duplicate prevention
- Retry on failure

---

## 3. Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | Recognition time | < 3 sec |
| NFR-02 | App load (cached) | < 2 sec |
| NFR-03 | Uptime | 99.9% |
| NFR-04 | HTTPS | Mandatory |
| NFR-05 | Encryption | AES-256 |

---

## 4. Data Models

### Employee
```
id, emp_code, name, email, department, 
face_descriptor (encrypted), status, timestamps
```

### Attendance
```
id, emp_id, date, time, latitude, longitude,
device_id, photo, sync_status, timestamps
```

### User
```
id, username, password_hash, role, emp_id, is_active
```

---

## 5. Technology Stack

| Layer | Technology | License |
|-------|------------|---------|
| Frontend | React 18, Vite, TailwindCSS | MIT |
| Face | face-api.js | MIT |
| Offline | IndexedDB (idb), Workbox | MIT/ISC |
| Backend | FastAPI, SQLAlchemy | MIT |
| Database | PostgreSQL | PostgreSQL |
| Auth | python-jose, bcrypt | MIT |

---

## 6. Acceptance Criteria

- [ ] Face detection < 2 seconds
- [ ] 95%+ matching accuracy
- [ ] Offline attendance works
- [ ] Auto-sync on reconnect
- [ ] No data loss on refresh
- [ ] Admin can manage employees
- [ ] Reports exportable (Excel/PDF)

---

## 7. Constraints

- Device must have camera
- HTTPS required
- Browser: Chrome 80+ / Edge 80+
- 100MB local storage needed

---

**Status:** ✅ Production Ready
