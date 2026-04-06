"""Unit tests for formatter utilities."""
import pytest
from src.models.order import Order, OrderItem, OrderStatus
from src.models.customer import Customer, CustomerTier
from src.utils.formatters import (
    format_currency,
    format_order_summary,
    format_customer_info,
)


class TestFormatCurrency:
    """Tests for currency formatting."""

    def test_format_usd(self):
        assert format_currency(1234.56) == "$1,234.56"

    def test_format_usd_zero(self):
        assert format_currency(0.0) == "$0.00"

    def test_format_eur(self):
        assert format_currency(100.0, "EUR") == "€100.00"

    def test_format_gbp(self):
        assert format_currency(50.0, "GBP") == "£50.00"

    # TODO: Add test for unknown currency code
    # TODO: Add test for very large amount


class TestFormatOrderSummary:
    """Tests for order summary formatting."""

    def test_summary_contains_order_id(self):
        order = Order(id="ORD-00001", customer_id="C001")
        summary = format_order_summary(order)
        assert "ORD-00001" in summary

    def test_summary_contains_status(self):
        order = Order(id="ORD-00001", customer_id="C001")
        summary = format_order_summary(order)
        assert "PENDING" in summary

    # TODO: Add test that discount line appears when discount > 0
    # TODO: Add test that shipping line appears when shipping_cost > 0
    # TODO: Add test for order with multiple items


class TestFormatCustomerInfo:
    """Tests for customer info formatting."""

    def test_customer_info_contains_name(self):
        customer = Customer(id="C001", name="Alice Smith", email="alice@example.com")
        info = format_customer_info(customer)
        assert "Alice Smith" in info

    def test_customer_info_contains_email(self):
        customer = Customer(id="C001", name="Alice Smith", email="alice@example.com")
        info = format_customer_info(customer)
        assert "alice@example.com" in info

    # TODO: Add test that tier is shown in uppercase
    # TODO: Add test that total spent is formatted as currency
