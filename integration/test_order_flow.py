"""Integration tests for the complete order processing flow.

These tests exercise multiple modules together to validate end-to-end behavior.

NOTE FOR STUDENTS: These integration tests cover the happy path.
Use GitHub Copilot to add tests for error conditions, edge cases,
and additional scenarios (e.g., order with multiple products,
discounts applied at various tiers, etc.).
"""
import pytest
from src.models.customer import Customer, CustomerTier
from src.models.product import Product
from src.services.inventory_service import InventoryService
from src.services.pricing_service import PricingService
from src.services.order_service import OrderService
from src.models.order import OrderStatus


@pytest.fixture
def inventory():
    svc = InventoryService()
    svc.add_product(Product(id="P001", name="Widget", price=30.0, stock=50, category="Tools"))
    svc.add_product(Product(id="P002", name="Gadget", price=80.0, stock=10, category="Electronics"))
    svc.add_product(Product(id="P003", name="Doohickey", price=15.0, stock=3, category="Misc"))
    return svc


@pytest.fixture
def pricing():
    return PricingService()


@pytest.fixture
def order_service(inventory, pricing):
    return OrderService(inventory=inventory, pricing=pricing)


@pytest.fixture
def standard_customer():
    return Customer(id="C001", name="Alice", email="alice@example.com")


@pytest.fixture
def gold_customer():
    return Customer(
        id="C002", name="Bob", email="bob@example.com",
        tier=CustomerTier.GOLD, total_spent=6000.0
    )


class TestHappyPathOrderFlow:
    """Tests for the standard successful order flow."""

    def test_full_order_lifecycle(self, order_service, standard_customer, inventory):
        """Test creating, filling, confirming, and advancing an order."""
        # Create order
        order = order_service.create_order(standard_customer)
        assert order.status == OrderStatus.PENDING

        # Add items
        order_service.add_item_to_order(order, "P001", 2)
        assert len(order.items) == 1

        # Confirm order
        order_service.confirm_order(order, standard_customer)
        assert order.status == OrderStatus.CONFIRMED

        # Advance through pipeline
        order_service.advance_order(order.id)
        assert order.status == OrderStatus.PROCESSING

        order_service.advance_order(order.id)
        assert order.status == OrderStatus.SHIPPED

        order_service.advance_order(order.id)
        assert order.status == OrderStatus.DELIVERED

    def test_free_shipping_applied_on_large_order(
        self, order_service, standard_customer
    ):
        """Orders with subtotal >= $75 should get free shipping."""
        order = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order, "P002", 1)  # $80 gadget
        order_service.confirm_order(order, standard_customer)
        assert order.shipping_cost == 0.0

    def test_shipping_cost_applied_on_small_order(
        self, order_service, standard_customer
    ):
        """Orders with subtotal < $75 should incur a shipping charge."""
        order = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order, "P001", 1)  # $30 widget
        order_service.confirm_order(order, standard_customer)
        assert order.shipping_cost == pytest.approx(9.99)

    def test_gold_customer_gets_discount(self, order_service, gold_customer):
        """Gold tier customers should receive a 10% discount."""
        order = order_service.create_order(gold_customer)
        order_service.add_item_to_order(order, "P002", 1)  # $80 gadget
        order_service.confirm_order(order, gold_customer)
        # 10% of $80 = $8 discount, no shipping (>= $75)
        assert order.discount_amount == pytest.approx(8.0)
        assert order.total == pytest.approx(72.0)


class TestCancellationFlow:
    """Tests for order cancellation and inventory restoration."""

    def test_cancel_order_restores_inventory(
        self, order_service, standard_customer, inventory
    ):
        """Cancelling an order should restore reserved stock."""
        order = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order, "P003", 2)
        # Stock should be 1 now (3 - 2)
        assert inventory.get_product("P003").stock == 1

        order_service.cancel_order(order.id)
        # Stock should be restored to 3
        assert inventory.get_product("P003").stock == 3
        assert order.status == OrderStatus.CANCELLED

    # TODO: Add test for cancelling after confirm (should still restore stock)
    # TODO: Add test that cancelling a shipped order raises an error
    # TODO: Add test for placing multiple orders and verifying stock correctly


class TestEdgeCases:
    """Edge case integration tests."""

    def test_order_with_multiple_products(
        self, order_service, standard_customer, inventory
    ):
        """Order with multiple different products should sum correctly."""
        order = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order, "P001", 1)  # $30
        order_service.add_item_to_order(order, "P002", 1)  # $80
        assert order.subtotal == pytest.approx(110.0)

    def test_exhausting_stock_prevents_further_orders(
        self, order_service, standard_customer
    ):
        """After exhausting stock, further orders for that product should fail."""
        order1 = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order1, "P003", 3)  # Uses all 3 in stock

        order2 = order_service.create_order(standard_customer)
        with pytest.raises(ValueError):
            order_service.add_item_to_order(order2, "P003", 1)

    # TODO: Add integration test combining coupon codes with tier discounts
    # TODO: Add integration test for listing orders by customer
    # TODO: Add integration test for listing orders by status
