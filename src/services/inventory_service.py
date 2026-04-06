"""Inventory management service."""
from typing import Dict, List, Optional
from ..models.product import Product


class InventoryService:
    """Manages product inventory."""

    def __init__(self):
        self._products: Dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        """Add a new product to inventory."""
        if product.id in self._products:
            raise ValueError(f"Product with id {product.id!r} already exists")
        self._products[product.id] = product

    def get_product(self, product_id: str) -> Optional[Product]:
        """Retrieve a product by ID, or None if not found."""
        return self._products.get(product_id)

    def get_product_or_raise(self, product_id: str) -> Product:
        """Retrieve a product by ID, raising an error if not found."""
        product = self.get_product(product_id)
        if product is None:
            raise KeyError(f"Product not found: {product_id!r}")
        return product

    def list_products(self) -> List[Product]:
        """Return all products in inventory."""
        return list(self._products.values())

    def list_available_products(self) -> List[Product]:
        """Return only products that are currently in stock."""
        return [p for p in self._products.values() if p.is_available]

    def search_by_category(self, category: str) -> List[Product]:
        """Return products matching the given category (case-insensitive)."""
        return [
            p for p in self._products.values()
            if p.category.lower() == category.lower()
        ]

    def reserve_stock(self, product_id: str, quantity: int) -> None:
        """Reserve stock for a product (reduce available quantity)."""
        product = self.get_product_or_raise(product_id)
        product.reduce_stock(quantity)

    def restock_product(self, product_id: str, quantity: int) -> None:
        """Add stock back to a product."""
        product = self.get_product_or_raise(product_id)
        product.restock(quantity)

    def remove_product(self, product_id: str) -> Product:
        """Remove and return a product from inventory."""
        if product_id not in self._products:
            raise KeyError(f"Product not found: {product_id!r}")
        return self._products.pop(product_id)

    def get_low_stock_products(self, threshold: int = 5) -> List[Product]:
        """Return products with stock at or below the threshold."""
        return [p for p in self._products.values() if p.stock <= threshold]
