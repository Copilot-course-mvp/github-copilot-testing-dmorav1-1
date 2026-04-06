"""Unit tests for InventoryService."""
import pytest
from src.models.product import Product
from src.services.inventory_service import InventoryService


@pytest.fixture
def inventory():
    return InventoryService()


@pytest.fixture
def sample_product():
    return Product(id="P001", name="Laptop", price=999.99, stock=10, category="Electronics")


class TestAddAndGetProduct:
    """Tests for adding and retrieving products."""

    def test_add_and_retrieve_product(self, inventory, sample_product):
        inventory.add_product(sample_product)
        result = inventory.get_product("P001")
        assert result is sample_product

    def test_get_nonexistent_product_returns_none(self, inventory):
        assert inventory.get_product("MISSING") is None

    def test_get_or_raise_nonexistent_raises_key_error(self, inventory):
        with pytest.raises(KeyError):
            inventory.get_product_or_raise("MISSING")

    def test_add_duplicate_product_raises_error(self, inventory, sample_product):
        inventory.add_product(sample_product)
        duplicate = Product(id="P001", name="Other", price=1.0, stock=1, category="X")
        with pytest.raises(ValueError, match="already exists"):
            inventory.add_product(duplicate)

    # TODO: Add test for list_products returns all products
    # TODO: Add test for list_available_products excludes out-of-stock items


class TestStockManagement:
    """Tests for stock reservation and restocking."""

    def test_reserve_stock_reduces_product_stock(self, inventory, sample_product):
        inventory.add_product(sample_product)
        inventory.reserve_stock("P001", 3)
        assert inventory.get_product("P001").stock == 7

    def test_reserve_more_than_available_raises_error(self, inventory, sample_product):
        inventory.add_product(sample_product)
        with pytest.raises(ValueError, match="Insufficient stock"):
            inventory.reserve_stock("P001", 100)

    def test_restock_increases_product_stock(self, inventory, sample_product):
        inventory.add_product(sample_product)
        inventory.restock_product("P001", 5)
        assert inventory.get_product("P001").stock == 15

    # TODO: Add test for get_low_stock_products with threshold
    # TODO: Add test for search_by_category (case-insensitive)
    # TODO: Add test for remove_product


class TestInventoryListing:
    """Tests for inventory listing features."""

    def test_list_available_products(self, inventory):
        p1 = Product(id="P001", name="In Stock", price=10.0, stock=5, category="A")
        p2 = Product(id="P002", name="Out of Stock", price=20.0, stock=0, category="A")
        inventory.add_product(p1)
        inventory.add_product(p2)
        available = inventory.list_available_products()
        assert len(available) == 1
        assert available[0].id == "P001"
