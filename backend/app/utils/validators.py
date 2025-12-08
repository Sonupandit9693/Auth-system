import re

def is_valid_email(email: str)->bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_username(username: str)->bool:
    return 3 <= len(username) <= 50 and username.isalnum()

def is_strong_password(password: str)-> tuple[bool, str]:
    if len(password) < 12:
        return False, "Password must be at least 12 characters"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

    if not (has_upper and has_lower and has_digit and has_special):
        return False , "Password must contain uppercase, lowercase, digit, and special character"
    
    return True, "strong password"