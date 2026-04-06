"""Mathematical calculation utilities."""
from typing import List, Optional


def calculate_tax(amount: float, tax_rate_percent: float) -> float:
    """Calculate tax amount for a given subtotal and tax rate.
    
    Args:
        amount: The pre-tax amount.
        tax_rate_percent: The tax rate as a percentage (e.g., 8.5 for 8.5%).

    Returns:
        The tax amount rounded to 2 decimal places.

    Raises:
        ValueError: If amount is negative or tax_rate_percent is out of range.
    """
    if amount < 0:
        raise ValueError(f"Amount cannot be negative: {amount}")
    if not 0 <= tax_rate_percent <= 100:
        raise ValueError(
            f"Tax rate must be between 0 and 100: {tax_rate_percent}"
        )
    return round(amount * tax_rate_percent / 100, 2)


def calculate_average(values: List[float]) -> Optional[float]:
    """Calculate the arithmetic mean of a list of numbers.
    
    Returns None if the list is empty.
    """
    if not values:
        return None
    return sum(values) / len(values)


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate the percentage change between two values.
    
    Args:
        old_value: The original value.
        new_value: The new value.

    Returns:
        Percentage change (positive = increase, negative = decrease).

    Raises:
        ValueError: If old_value is zero (division by zero).
    """
    if old_value == 0:
        raise ValueError("Cannot calculate percentage change from zero")
    return ((new_value - old_value) / abs(old_value)) * 100


def calculate_compound_interest(
    principal: float, rate_percent: float, periods: int
) -> float:
    """Calculate compound interest total (principal + interest).

    Args:
        principal: The initial amount.
        rate_percent: Interest rate per period as a percentage.
        periods: Number of compounding periods.

    Returns:
        Total amount after compound interest.
    """
    if principal < 0:
        raise ValueError(f"Principal cannot be negative: {principal}")
    if rate_percent < 0:
        raise ValueError(f"Rate cannot be negative: {rate_percent}")
    if periods < 0:
        raise ValueError(f"Periods cannot be negative: {periods}")
    rate = rate_percent / 100
    return round(principal * (1 + rate) ** periods, 2)


def apply_discount(amount: float, discount_percent: float) -> float:
    """Apply a percentage discount to an amount.

    Args:
        amount: The original amount.
        discount_percent: Discount as a percentage (0-100).

    Returns:
        The discounted amount.
    """
    if amount < 0:
        raise ValueError(f"Amount cannot be negative: {amount}")
    if not 0 <= discount_percent <= 100:
        raise ValueError(
            f"Discount percent must be between 0 and 100: {discount_percent}"
        )
    return round(amount * (1 - discount_percent / 100), 2)
