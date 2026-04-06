"""Unit tests for validator utilities."""
import pytest
from src.utils.validators import (
    validate_email,
    validate_price,
    validate_quantity,
    validate_product_id,
    validate_coupon_code,
    validate_customer_name,
)


class TestEmailValidator:
    """Tests for email validation."""

    def test_valid_email(self):
        assert validate_email("user@example.com") is True

    def test_valid_email_with_subdomain(self):
        assert validate_email("user@mail.example.co.uk") is True

    def test_missing_at_sign(self):
        assert validate_email("userexample.com") is False

    def test_missing_domain(self):
        assert validate_email("user@") is False

    def test_empty_string(self):
        assert validate_email("") is False

    # TODO: Add test for None input
    # TODO: Add test for email with spaces
    # TODO: Add test for email with special characters in local part


class TestPriceValidator:
    """Tests for price validation."""

    def test_valid_price_positive(self):
        assert validate_price(9.99) is True

    def test_valid_price_zero(self):
        assert validate_price(0.0) is True

    def test_invalid_price_negative(self):
        assert validate_price(-1.0) is False

    # TODO: Add test for string input
    # TODO: Add test for very large price


class TestQuantityValidator:
    """Tests for quantity validation."""

    def test_valid_quantity(self):
        assert validate_quantity(5) is True

    def test_invalid_quantity_zero(self):
        assert validate_quantity(0) is False

    def test_invalid_quantity_negative(self):
        assert validate_quantity(-3) is False

    # TODO: Add test for float input (should return False)
    # TODO: Add test for very large quantity


class TestProductIdValidator:
    """Tests for product ID validation."""

    def test_valid_product_id(self):
        assert validate_product_id("P001") is True

    def test_valid_product_id_with_dashes(self):
        assert validate_product_id("PROD-001-XL") is True

    def test_empty_product_id(self):
        assert validate_product_id("") is False

    # TODO: Add test for product ID starting with special character
    # TODO: Add test for product ID that is too long (>50 chars)
