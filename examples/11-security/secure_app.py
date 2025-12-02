"""
Reel Security Example - Authentication and Authorization

This example demonstrates how to add security to your Reel applications:
1. Session-based authentication
2. Role-based authorization
3. Input validation and sanitization
4. Secure function exposure patterns

⚠️ IMPORTANT: This is a demonstration example. In production:
   - Use bcrypt/argon2 for password hashing
   - Use secure session storage (Redis, database)
   - Enable HTTPS/WSS
   - Implement CSRF protection
   - Add rate limiting
   - Use environment variables for secrets
"""

import eel
import os
import secrets
import re
from functools import wraps
from typing import Dict, Optional, List, Any

# Initialize Reel
eel.init('web')

# Simple in-memory session store (use Redis/database in production)
_sessions: Dict[str, Dict[str, Any]] = {}

# Demo users (in production, use a database with hashed passwords)
_users = {
    'admin': {
        'password': 'admin123',  # In production: use bcrypt.hashpw()
        'roles': ['admin', 'user'],
        'name': 'Administrator'
    },
    'user': {
        'password': 'user123',
        'roles': ['user'],
        'name': 'Regular User'
    }
}

def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Get session data by session ID."""
    return _sessions.get(session_id)

def create_session(username: str) -> str:
    """Create a new session for authenticated user."""
    session_id = secrets.token_urlsafe(32)
    _sessions[session_id] = {
        'username': username,
        'roles': _users[username]['roles'],
        'name': _users[username]['name']
    }
    return session_id

def destroy_session(session_id: str) -> None:
    """Destroy a session."""
    if session_id in _sessions:
        del _sessions[session_id]

def require_auth(roles: Optional[List[str]] = None):
    """
    Decorator to require authentication and optional role-based authorization.

    Usage:
        @eel.expose
        @require_auth()
        def protected_function():
            pass

        @eel.expose
        @require_auth(roles=['admin'])
        def admin_only_function():
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(session_id: str, *args, **kwargs):
            # Validate session
            session = get_session(session_id)
            if not session:
                return {'error': 'Unauthorized', 'code': 401}

            # Check role-based authorization if required
            if roles:
                user_roles = session.get('roles', [])
                if not any(role in user_roles for role in roles):
                    return {'error': 'Forbidden - insufficient permissions', 'code': 403}

            # Call the original function with session context
            return func(session, *args, **kwargs)

        return wrapper
    return decorator

def validate_input(value: str, pattern: str, max_length: int = 100) -> bool:
    """Validate input against pattern and length constraints."""
    if not value or len(value) > max_length:
        return False
    return bool(re.match(pattern, value))

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@eel.expose
def login(username: str, password: str) -> Dict[str, Any]:
    """
    Authenticate user and create session.

    Returns session_id on success or error object on failure.
    """
    # Input validation
    if not validate_input(username, r'^[a-zA-Z0-9_]{3,20}$'):
        return {'error': 'Invalid username format', 'code': 400}

    # Check credentials
    user = _users.get(username)
    if not user or user['password'] != password:
        return {'error': 'Invalid username or password', 'code': 401}

    # Create session
    session_id = create_session(username)

    return {
        'success': True,
        'session_id': session_id,
        'user': {
            'username': username,
            'name': user['name'],
            'roles': user['roles']
        }
    }

@eel.expose
def logout(session_id: str) -> Dict[str, Any]:
    """Logout user and destroy session."""
    destroy_session(session_id)
    return {'success': True}

@eel.expose
@require_auth()
def get_current_user(session: Dict[str, Any]) -> Dict[str, Any]:
    """Get current authenticated user information."""
    return {
        'username': session['username'],
        'name': session['name'],
        'roles': session['roles']
    }

# ============================================================================
# PROTECTED ENDPOINTS - USER LEVEL
# ============================================================================

@eel.expose
@require_auth()
def get_user_data(session: Dict[str, Any]) -> Dict[str, Any]:
    """Get data accessible to authenticated users."""
    return {
        'message': f"Hello {session['name']}! This is user-level data.",
        'data': [
            {'id': 1, 'title': 'User Dashboard'},
            {'id': 2, 'title': 'Profile Settings'},
            {'id': 3, 'title': 'Activity Log'}
        ]
    }

@eel.expose
@require_auth()
def update_profile(session: Dict[str, Any], display_name: str) -> Dict[str, Any]:
    """Update user profile (with input validation)."""
    # Validate input
    if not validate_input(display_name, r'^[a-zA-Z0-9\s]{3,50}$', max_length=50):
        return {'error': 'Invalid display name format', 'code': 400}

    # In production: update database
    return {
        'success': True,
        'message': f'Profile updated for {session["username"]}',
        'new_name': display_name
    }

# ============================================================================
# PROTECTED ENDPOINTS - ADMIN LEVEL
# ============================================================================

@eel.expose
@require_auth(roles=['admin'])
def get_admin_data(session: Dict[str, Any]) -> Dict[str, Any]:
    """Get admin-only data."""
    return {
        'message': f"Admin access granted for {session['name']}",
        'data': [
            {'id': 1, 'title': 'System Settings'},
            {'id': 2, 'title': 'User Management'},
            {'id': 3, 'title': 'Security Logs'},
            {'id': 4, 'title': 'Database Backup'}
        ]
    }

@eel.expose
@require_auth(roles=['admin'])
def get_system_stats(session: Dict[str, Any]) -> Dict[str, Any]:
    """Get system statistics (admin only)."""
    return {
        'active_sessions': len(_sessions),
        'total_users': len(_users),
        'admin': session['username']
    }

@eel.expose
@require_auth(roles=['admin'])
def execute_admin_action(session: Dict[str, Any], action: str) -> Dict[str, Any]:
    """
    Execute administrative action with validation.

    This demonstrates safe command execution patterns.
    """
    # Whitelist allowed actions
    allowed_actions = {
        'backup': 'Database backup initiated',
        'clear_cache': 'Cache cleared successfully',
        'reload_config': 'Configuration reloaded'
    }

    if action not in allowed_actions:
        return {'error': f'Action not allowed: {action}', 'code': 403}

    # In production: execute the actual action
    return {
        'success': True,
        'message': allowed_actions[action],
        'executor': session['username']
    }

# ============================================================================
# PUBLIC ENDPOINTS (No authentication required)
# ============================================================================

@eel.expose
def get_public_info() -> Dict[str, str]:
    """Get public information (no authentication required)."""
    return {
        'app_name': 'Reel Security Demo',
        'version': '1.0.0',
        'message': 'This endpoint is publicly accessible'
    }

# ============================================================================
# START APPLICATION
# ============================================================================

if __name__ == '__main__':
    print("🎬 Reel Security Example")
    print("=" * 50)
    print("\n📝 Test Credentials:")
    print("   Admin: admin / admin123")
    print("   User:  user / user123")
    print("\n⚠️  Security Features Demonstrated:")
    print("   ✓ Session-based authentication")
    print("   ✓ Role-based authorization")
    print("   ✓ Input validation and sanitization")
    print("   ✓ Secure function exposure patterns")
    print("\n🌐 Starting application...")
    print("=" * 50)

    # Set debug mode for development (shows detailed errors)
    os.environ['EEL_DEBUG'] = '1'

    # Start Reel with security-focused configuration
    eel.start(
        'secure_app.html',
        size=(1000, 700),
        port=8000,
        mode='chrome',  # Use 'chrome-app' mode for standalone app
        cmdline_args=[
            '--disable-http-cache',  # Disable cache during development
        ]
    )
