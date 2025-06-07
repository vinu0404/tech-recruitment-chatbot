import re

def validate_email(email):
    """Validate email format"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

def validate_phone(phone):
    """Validate phone number format"""
    phone_pattern = r'^\+?1?\d{9,15}$|^(\+\d{1,3}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$'
    return bool(re.match(phone_pattern, phone.strip().replace(' ', '')))