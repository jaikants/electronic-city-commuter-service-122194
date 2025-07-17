"""
Utility functions: password hashing, JWT token creation/verification, and auth decorators.
"""

import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os

def hash_password(password):
    """Hash password for storing in db."""
    return generate_password_hash(password)

def verify_password(password, hash_):
    """Verify password hash."""
    return check_password_hash(hash_, password)

def create_token(identity, user_type, expires_in=86400):
    """Generate JWT token with identity and user_type."""
    payload = {
        "identity": identity,
        "user_type": user_type,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    }
    jwt_secret = os.environ.get('JWT_SECRET', 'change_this_secret')
    token = jwt.encode(payload, jwt_secret, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def decode_token(token):
    """Decode JWT, return payload or None."""
    jwt_secret = os.environ.get('JWT_SECRET', 'change_this_secret')
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_identity_from_request():
    """Get (identity, user_type) from the Authorization header token."""
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        return None, None
    token = auth.split(" ")[1]
    payload = decode_token(token)
    if payload is None:
        return None, None
    return payload.get("identity"), payload.get("user_type")

def login_required(user_type=None):
    """
    Decorator for routes that require JWT auth.
    Optionally restricts to a certain user type.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            identity, utype = get_identity_from_request()
            if identity is None:
                return jsonify({"message": "Unauthorized"}), 401
            if user_type and utype != user_type:
                return jsonify({"message": "Forbidden: Wrong user type"}), 403
            return func(identity, *args, **kwargs)
        return wrapper
    return decorator
