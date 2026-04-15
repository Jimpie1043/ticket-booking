import re

def validate_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def validate_password(password: str) -> bool:
    return len(password) >= 8


def sanitize_string(value: str) -> str:
    if not value:
        return ""
    return value.strip()