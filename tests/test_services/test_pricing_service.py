"""Unit tests for PricingService."""
import pytest
from src.models.customer import Customer, CustomerTier
from src.services.pricing_service import PricingService


@pytest.fixture
def pricing():
    return PricingService()


@pytest.fixture
def standard_customer():
    return Customer(id="C001", name="Alice", email="alice@example.com")


@pytest.fixture
def gold_customer():
    return Customer(
        id="C002", name="Bob", email="bob@example.com", tier=CustomerTier.GOLD
    )


class TestShippingCalculation:
    """Tests for shipping cost logic."""

    def test_free_shipping_above_threshold(self, pricing):
        assert pricing.calculate_shipping(75.0) == 0.0

    def test_free_shipping_above_threshold_large(self, pricing):
        assert pricing.calculate_shipping(200.0) == 0.0

    def test_shipping_cost_below_threshold(self, pricing):
        assert pricing.calculate_shipping(50.0) == pytest.approx(9.99)

    def test_shipping_cost_at_zero(self, pricing):
        assert pricing.calculate_shipping(0.0) == pytest.approx(9.99)

    # TODO: Add test for negative subtotal raises ValueError


class TestCustomerDiscount:
    """Tests for customer tier discount calculation."""

    def test_no_discount_for_standard_customer(self, pricing, standard_customer):
        discount = pricing.calculate_customer_discount(100.0, standard_customer)
        assert discount == 0.0

    def test_gold_customer_gets_ten_percent(self, pricing, gold_customer):
        discount = pricing.calculate_customer_discount(100.0, gold_customer)
        assert discount == 10.0

    # TODO: Add test for PLATINUM customer discount
    # TODO: Add test for SILVER customer discount


class TestCouponCode:
    """Tests for coupon code application."""

    def test_valid_coupon_save10(self, pricing):
        assert pricing.apply_coupon(100.0, "SAVE10") == 10.0

    def test_valid_coupon_halfoff(self, pricing):
        assert pricing.apply_coupon(200.0, "HALFOFF") == 100.0

    def test_invalid_coupon_returns_zero(self, pricing):
        assert pricing.apply_coupon(100.0, "BADCODE") == 0.0

    def test_coupon_is_case_insensitive(self, pricing):
        assert pricing.apply_coupon(100.0, "save10") == 10.0

    # TODO: Add test for WELCOME coupon (5%)
    # TODO: Add test for SAVE20 coupon (20%)


class TestBulkDiscount:
    """Tests for bulk purchase discounts."""

    def test_no_bulk_discount_below_threshold(self, pricing):
        assert pricing.calculate_bulk_discount(100.0, 4) == 0.0

    def test_bulk_discount_at_threshold(self, pricing):
        assert pricing.calculate_bulk_discount(100.0, 5) == 10.0

    # TODO: Add test for bulk discount above threshold (e.g., 10 items)
