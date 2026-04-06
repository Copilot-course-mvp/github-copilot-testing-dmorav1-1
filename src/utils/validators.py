"""Input validation utilities."""
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """Return True if email is a valid format."""
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_price(price: float) -> bool:
    """Return True if price is a non-negative number."""
    if not isinstance(price, (int, float)):
        return False
    return price >= 0


def validate_quantity(quantity: int) -> bool:
    """Return True if quantity is a positive integer."""
    if not isinstance(quantity, int):
        return False
    return quantity > 0


def validate_product_id(product_id: str) -> bool:
    """Return True if product_id matches expected format (alphanumeric with dashes)."""
    if not product_id or not isinstance(product_id, str):
        return False
    pattern = r'^[A-Za-z0-9][A-Za-z0-9\-_]{0,49}$'
    return bool(re.match(pattern, product_id))


def validate_coupon_code(coupon_code: str) -> bool:
    """Return True if coupon code is uppercase letters only, 4-10 chars."""
    if not coupon_code or not isinstance(coupon_code, str):
        return False
    pattern = r'^[A-Z0-9]{4,10}$'
    return bool(re.match(pattern, coupon_code.upper()))


def validate_customer_name(name: str) -> bool:
    """Return True if name is non-empty and contains only valid characters."""
    if not name or not isinstance(name, str):
        return False
    stripped = name.strip()
    if not stripped:
        return False
    return len(stripped) >= 2 and len(stripped) <= 100
