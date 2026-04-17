import re
from flask_talisman import Talisman
from markupsafe import escape


def validate_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def validate_password(password: str) -> bool:
    return 8 <= len(password) <= 64


def sanitize_string(value: str) -> str:
    if not value:
        return ""
    return escape(value.strip())


def init_security(app):
    Talisman(
        app,
        content_security_policy={
            "default-src": "'self'",
            "script-src": ["'self'"],
            "style-src": ["'self'", "'unsafe-inline'"],
            "img-src": ["'self'", "data:"]
        },
        
        force_https=app.config.get("FORCE_HTTPS", False),
        session_cookie_secure=app.config.get("SESSION_COOKIE_SECURE", False),
        session_cookie_http_only=app.config.get("SESSION_COOKIE_HTTPONLY", True)
    )