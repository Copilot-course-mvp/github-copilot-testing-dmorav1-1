"""Customer model for the e-commerce system."""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class CustomerTier(Enum):
    """Customer loyalty tier."""
    STANDARD = "standard"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"


@dataclass
class Customer:
    """Represents a customer in the system."""

    id: str
    name: str
    email: str
    tier: CustomerTier = CustomerTier.STANDARD
    total_spent: float = 0.0
    order_count: int = 0
    address: Optional[str] = None

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Customer name cannot be empty")
        if "@" not in self.email:
            raise ValueError(f"Invalid email address: {self.email}")
        if self.total_spent < 0:
            raise ValueError(f"Total spent cannot be negative: {self.total_spent}")
        if self.order_count < 0:
            raise ValueError(f"Order count cannot be negative: {self.order_count}")

    @property
    def tier_discount_percent(self) -> float:
        """Return the discount percentage based on customer tier."""
        discounts = {
            CustomerTier.STANDARD: 0.0,
            CustomerTier.SILVER: 5.0,
            CustomerTier.GOLD: 10.0,
            CustomerTier.PLATINUM: 15.0,
        }
        return discounts[self.tier]

    def update_tier(self) -> None:
        """Update customer tier based on total spending."""
        if self.total_spent >= 10000:
            self.tier = CustomerTier.PLATINUM
        elif self.total_spent >= 5000:
            self.tier = CustomerTier.GOLD
        elif self.total_spent >= 1000:
            self.tier = CustomerTier.SILVER
        else:
            self.tier = CustomerTier.STANDARD

    def record_purchase(self, amount: float) -> None:
        """Record a purchase and update tier accordingly."""
        if amount <= 0:
            raise ValueError(f"Purchase amount must be positive: {amount}")
        self.total_spent += amount
        self.order_count += 1
        self.update_tier()

    def __repr__(self) -> str:
        return f"Customer(id={self.id!r}, name={self.name!r}, tier={self.tier.value})"
