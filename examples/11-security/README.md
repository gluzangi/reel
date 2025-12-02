# 🔒 Reel Security Example

This example demonstrates how to implement **authentication and authorization** in Reel applications.

## 🎯 What This Example Demonstrates

### 1. Session-Based Authentication
- User login with credential validation
- Secure session management using session tokens
- Session cleanup on logout

### 2. Role-Based Authorization
- User roles (user, admin)
- `@require_auth()` decorator for protected functions
- Role-based access control for admin-only features

### 3. Input Validation
- Pattern-based validation using regex
- Maximum length constraints
- Sanitized error messages

### 4. Secure Function Exposure
- Whitelisting allowed actions
- Safe command execution patterns
- Protection against code injection

## 🚀 How to Run

### Quick Start

```bash
# From the examples/11-security directory
python secure_app.py
```

The application will open in Chrome app mode at http://localhost:8000

### Using Environment Variables (Recommended)

```bash
# 1. Copy the example environment file
cp .env.example .env

# 2. Edit .env with your configuration
# Change SECRET_KEY, adjust timeouts, etc.

# 3. Install python-dotenv (optional but recommended)
pip install python-dotenv

# 4. Run the application
python secure_app.py
```

**Available environment variables:**
- `EEL_DEBUG` - Enable detailed errors (1=on, 0=off)
- `EEL_ALLOWED_ORIGINS` - Comma-separated allowed origins
- `SECRET_KEY` - Session encryption key
- `SESSION_TIMEOUT` - Session timeout in seconds
- `EEL_HOST` - Server host (default: localhost)
- `EEL_PORT` - Server port (default: 8000)

## 🔑 Test Credentials

**Admin User:**
- Username: `admin`
- Password: `admin123`
- Roles: admin, user

**Regular User:**
- Username: `user`
- Password: `user123`
- Roles: user

## 📋 Features to Try

### As Regular User:
1. Login with user credentials
2. Access user dashboard
3. Load user-level data
4. Update profile (with validation)
5. Try to access admin features (will be denied)

### As Admin:
1. Login with admin credentials
2. Access both user and admin dashboards
3. View system statistics
4. Execute admin-only actions
5. See all available features

### Public Access:
- Click "Load Public Data" before logging in
- This demonstrates endpoints that don't require authentication

## 🔐 Security Patterns Demonstrated

### 1. Authentication Decorator

```python
@eel.expose
@require_auth()
def protected_function(session, *args):
    # session contains authenticated user info
    return f"Hello {session['username']}"
```

### 2. Role-Based Authorization

```python
@eel.expose
@require_auth(roles=['admin'])
def admin_only_function(session, *args):
    # Only admin users can call this
    return "Admin access granted"
```

### 3. Input Validation

```python
def validate_input(value: str, pattern: str, max_length: int = 100) -> bool:
    """Validate input against pattern and length constraints."""
    if not value or len(value) > max_length:
        return False
    return bool(re.match(pattern, value))
```

### 4. Safe Action Whitelisting

```python
# Whitelist allowed actions instead of executing arbitrary commands
allowed_actions = {
    'backup': 'Database backup initiated',
    'clear_cache': 'Cache cleared successfully'
}

if action not in allowed_actions:
    return {'error': f'Action not allowed: {action}'}
```

## ⚠️ Important Security Notes

This is a **demonstration example** for learning purposes. For **production use**, you must:

### 1. Password Security
```bash
# Install bcrypt
pip install bcrypt

# Use in your code
import bcrypt

# Hash passwords
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Verify passwords
if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
    # Password correct
```

### 2. Session Storage
- Use Redis or database for session storage (not in-memory)
- Set session expiration times
- Implement session rotation on privilege escalation

### 3. HTTPS/WSS
```python
# Enable HTTPS
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('cert.pem', 'key.pem')

# Configure Reel to use HTTPS
# (requires custom Bottle configuration)
```

### 4. CSRF Protection
```python
# Add CSRF tokens to forms
import secrets

csrf_token = secrets.token_urlsafe(32)

# Validate on submission
if submitted_token != session['csrf_token']:
    return {'error': 'CSRF validation failed'}
```

### 5. Rate Limiting
```python
from functools import wraps
import time

def rate_limit(max_calls=5, time_window=60):
    """Limit function calls per time window."""
    calls = {}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            key = args[0]  # session_id

            if key not in calls:
                calls[key] = []

            # Remove old calls
            calls[key] = [t for t in calls[key] if now - t < time_window]

            if len(calls[key]) >= max_calls:
                return {'error': 'Rate limit exceeded'}

            calls[key].append(now)
            return func(*args, **kwargs)

        return wrapper
    return decorator

@eel.expose
@rate_limit(max_calls=10, time_window=60)
@require_auth()
def rate_limited_function(session):
    pass
```

### 6. Environment Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')
```

## 📚 Additional Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Reel Security Analysis](../../docs/04-SECURITY_ANALYSIS.md)

## 🐛 Testing Security

### Test Authentication
```bash
# Try accessing protected functions without session
# Expected: Error 401 Unauthorized
```

### Test Authorization
```bash
# Login as regular user
# Try to access admin-only functions
# Expected: Error 403 Forbidden
```

### Test Input Validation
```bash
# Try invalid usernames (special characters, too long)
# Expected: Error 400 Bad Request
```

### Test Public Endpoints
```bash
# Access public endpoints without login
# Expected: Success
```

## 🔄 Next Steps

After understanding this example:

1. **Read**: [Security Analysis](../../docs/04-SECURITY_ANALYSIS.md)
2. **Implement**: Production-grade authentication in your app
3. **Add**: HTTPS/WSS support for network access
4. **Test**: Use security testing tools (OWASP ZAP, Burp Suite)
5. **Monitor**: Log authentication events and failed attempts

## 💡 Key Takeaways

✅ **Always validate inputs** - Never trust client data
✅ **Use strong passwords** - Hash with bcrypt/argon2
✅ **Implement authorization** - Not just authentication
✅ **Validate sessions** - Check on every protected request
✅ **Sanitize errors** - Don't leak sensitive information
✅ **Use HTTPS** - For any network-accessible deployment
✅ **Log security events** - Monitor for attacks

---

**Remember**: Security is not a feature, it's a requirement. This example provides a foundation, but production applications need comprehensive security reviews and testing.

For questions or security concerns, see [docs/04-SECURITY_ANALYSIS.md](../../docs/04-SECURITY_ANALYSIS.md)
