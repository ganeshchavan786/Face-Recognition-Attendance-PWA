# Security Guidelines

## Face Recognition Offline Attendance PWA

---

## 1. Authentication Security

### JWT Configuration
- **Algorithm:** HS256
- **Expiry:** 1 hour (access token)
- **Refresh:** 7 days (refresh token)
- **Secret:** Min 256-bit random key

### Password Policy
- Minimum 8 characters
- Must include uppercase, lowercase, number
- Hashed with bcrypt (cost factor: 12)

---

## 2. Data Encryption

### Face Descriptors
```python
# AES-256 encryption for face data
from cryptography.fernet import Fernet

# Key stored in environment variable (never in code)
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

def encrypt_descriptor(descriptor: list) -> bytes:
    f = Fernet(ENCRYPTION_KEY)
    data = json.dumps(descriptor).encode()
    return f.encrypt(data)

def decrypt_descriptor(encrypted: bytes) -> list:
    f = Fernet(ENCRYPTION_KEY)
    data = f.decrypt(encrypted)
    return json.loads(data.decode())
```

### Data at Rest
- Database: Encrypted columns for sensitive data
- Backups: Encrypted with GPG

### Data in Transit
- HTTPS mandatory (TLS 1.3)
- HSTS enabled

---

## 3. Role-Based Access Control (RBAC)

| Permission | ADMIN | SUPERVISOR | EMPLOYEE |
|------------|-------|------------|----------|
| Mark own attendance | ✓ | ✓ | ✓ |
| View own history | ✓ | ✓ | ✓ |
| View team data | ✓ | ✓ | ✗ |
| Manage employees | ✓ | ✗ | ✗ |
| Enroll faces | ✓ | ✗ | ✗ |
| Export reports | ✓ | ✓ | ✗ |
| System settings | ✓ | ✗ | ✗ |

---

## 4. Anti-Fraud Measures

### Liveness Detection
- Eye blink detection
- Random head movement prompts
- Photo/video rejection

### Device Binding
- UUID generated per device
- Attendance linked to device
- Alerts on device change

### Time Window Lock
- Configurable attendance window
- Reject out-of-window attempts

### Duplicate Prevention
- One attendance per employee per day
- Server-side validation

---

## 5. API Security

### Rate Limiting
```python
# 100 requests per minute per IP
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/api/auth/login")
@limiter.limit("5/minute")  # Stricter for login
async def login():
    pass
```

### Input Validation
- Pydantic schemas for all inputs
- SQL injection prevention (ORM)
- XSS prevention (sanitization)

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

---

## 6. IndexedDB Security (PWA)

- Data encrypted before storage
- Auto-clear on logout
- No sensitive data in localStorage

---

## 7. Audit Logging

Log all:
- Login attempts (success/failure)
- Attendance records
- Admin actions
- Face enrollment
- Data exports

---

## 8. Compliance

- **IT Act 2000** (India)
- **Data Privacy Guidelines**
- **Government Digital Standards**

---

## 9. Security Checklist

- [ ] HTTPS enabled
- [ ] Strong JWT secret
- [ ] Face data encrypted
- [ ] RBAC implemented
- [ ] Rate limiting active
- [ ] Input validation
- [ ] CORS configured
- [ ] Audit logging
- [ ] Regular backups
- [ ] Security updates applied
