"""Unit tests for OrderService.

NOTE FOR STUDENTS: This file has significant gaps in test coverage.
Use GitHub Copilot to complete the test suite.
"""
import pytest
from src.models.customer import Customer
from src.models.product import Product
from src.models.order import OrderStatus
from src.services.inventory_service import InventoryService
from src.services.pricing_service import PricingService
from src.services.order_service import OrderService


@pytest.fixture
def inventory():
    svc = InventoryService()
    svc.add_product(Product(id="P001", name="Widget", price=25.0, stock=20, category="Tools"))
    svc.add_product(Product(id="P002", name="Gadget", price=50.0, stock=5, category="Electronics"))
    return svc


@pytest.fixture
def pricing():
    return PricingService()


@pytest.fixture
def order_service(inventory, pricing):
    return OrderService(inventory=inventory, pricing=pricing)


@pytest.fixture
def customer():
    return Customer(id="C001", name="Alice", email="alice@example.com")


class TestOrderCreation:
    """Tests for order creation."""

    def test_create_order_returns_order(self, order_service, customer):
        order = order_service.create_order(customer)
        assert order is not None
        assert order.customer_id == customer.id
        assert order.status == OrderStatus.PENDING

    def test_order_ids_are_unique(self, order_service, customer):
        order1 = order_service.create_order(customer)
        order2 = order_service.create_order(customer)
        assert order1.id != order2.id

    # TODO: Add test for create_order generates sequential IDs


class TestAddItemToOrder:
    """Tests for adding items to orders."""

    def test_add_item_to_order_updates_stock(self, order_service, customer, inventory):
        order = order_service.create_order(customer)
        order_service.add_item_to_order(order, "P001", 3)
        assert inventory.get_product("P001").stock == 17

    def test_add_item_creates_order_item(self, order_service, customer):
        order = order_service.create_order(customer)
        order_service.add_item_to_order(order, "P001", 2)
        assert len(order.items) == 1
        assert order.items[0].quantity == 2

    def test_add_nonexistent_product_raises_error(self, order_service, customer):
        order = order_service.create_order(customer)
        with pytest.raises(KeyError):
            order_service.add_item_to_order(order, "NOTEXIST", 1)

    # TODO: Add test for adding out-of-stock product raises ValueError
    # TODO: Add test for requesting more than available stock raises ValueError


class TestConfirmAndCancel:
    """Tests for confirming and cancelling orders."""

    def test_confirm_order_changes_status(self, order_service, customer):
        order = order_service.create_order(customer)
        order_service.add_item_to_order(order, "P001", 1)
        order_service.confirm_order(order, customer)
        assert order.status == OrderStatus.CONFIRMED

    def test_cancel_order_restores_stock(self, order_service, customer, inventory):
        order = order_service.create_order(customer)
        order_service.add_item_to_order(order, "P001", 5)
        order_service.cancel_order(order.id)
        # stock should be restored to original 20
        assert inventory.get_product("P001").stock == 20

    # TODO: Add test for cancelling a non-existent order raises KeyError
    # TODO: Add test for advancing order through statuses
