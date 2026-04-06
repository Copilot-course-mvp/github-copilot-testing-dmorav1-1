"""Product model for the e-commerce system."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Product:
    """Represents a product available for purchase."""

    id: str
    name: str
    price: float
    stock: int
    category: str
    description: Optional[str] = None
    discount_percent: float = 0.0

    def __post_init__(self):
        if self.price < 0:
            raise ValueError(f"Price cannot be negative: {self.price}")
        if self.stock < 0:
            raise ValueError(f"Stock cannot be negative: {self.stock}")
        if not 0 <= self.discount_percent <= 100:
            raise ValueError(
                f"Discount percent must be between 0 and 100: {self.discount_percent}"
            )
        if not self.name or not self.name.strip():
            raise ValueError("Product name cannot be empty")

    @property
    def discounted_price(self) -> float:
        """Return the price after applying the discount."""
        return self.price * (1 - self.discount_percent / 100)

    @property
    def is_available(self) -> bool:
        """Return True if the product is in stock."""
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """Reduce stock by the given quantity."""
        if quantity <= 0:
            raise ValueError(f"Quantity must be positive: {quantity}")
        if quantity > self.stock:
            raise ValueError(
                f"Insufficient stock: requested {quantity}, available {self.stock}"
            )
        self.stock -= quantity

    def restock(self, quantity: int) -> None:
        """Add stock by the given quantity."""
        if quantity <= 0:
            raise ValueError(f"Quantity must be positive: {quantity}")
        self.stock += quantity

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r}, price={self.price}, stock={self.stock})"
