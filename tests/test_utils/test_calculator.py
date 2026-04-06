"""Unit tests for calculator utilities."""
import pytest
from src.utils.calculator import (
    calculate_tax,
    calculate_average,
    calculate_percentage_change,
    calculate_compound_interest,
    apply_discount,
)


class TestCalculateTax:
    """Tests for tax calculation."""

    def test_tax_calculation_basic(self):
        assert calculate_tax(100.0, 10.0) == 10.0

    def test_tax_calculation_zero_rate(self):
        assert calculate_tax(100.0, 0.0) == 0.0

    def test_tax_calculation_zero_amount(self):
        assert calculate_tax(0.0, 8.5) == 0.0

    def test_negative_amount_raises_error(self):
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            calculate_tax(-50.0, 10.0)

    def test_tax_rate_over_100_raises_error(self):
        with pytest.raises(ValueError, match="Tax rate must be between"):
            calculate_tax(100.0, 101.0)

    # TODO: Add test for fractional tax rate (e.g., 8.75%)
    # TODO: Add test for negative tax rate raises ValueError
    # TODO: Add test for 100% tax rate


class TestCalculateAverage:
    """Tests for average calculation."""

    def test_average_of_list(self):
        assert calculate_average([1.0, 2.0, 3.0]) == 2.0

    def test_average_of_single_value(self):
        assert calculate_average([42.0]) == 42.0

    def test_average_of_empty_list(self):
        assert calculate_average([]) is None

    # TODO: Add test for list with negative values
    # TODO: Add test for large list (performance/correctness check)


class TestCalculatePercentageChange:
    """Tests for percentage change calculation."""

    def test_positive_change(self):
        assert calculate_percentage_change(100.0, 120.0) == pytest.approx(20.0)

    def test_negative_change(self):
        assert calculate_percentage_change(100.0, 80.0) == pytest.approx(-20.0)

    def test_no_change(self):
        assert calculate_percentage_change(100.0, 100.0) == pytest.approx(0.0)

    def test_zero_old_value_raises_error(self):
        with pytest.raises(ValueError, match="Cannot calculate percentage change from zero"):
            calculate_percentage_change(0.0, 50.0)

    # TODO: Add test for change from negative value


class TestApplyDiscount:
    """Tests for discount application."""

    def test_apply_twenty_percent_discount(self):
        assert apply_discount(100.0, 20.0) == 80.0

    def test_apply_zero_discount(self):
        assert apply_discount(100.0, 0.0) == 100.0

    def test_apply_full_discount(self):
        assert apply_discount(100.0, 100.0) == 0.0

    def test_negative_amount_raises_error(self):
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            apply_discount(-10.0, 10.0)

    # TODO: Add test for discount > 100 raises ValueError
    # TODO: Add test for discount < 0 raises ValueError


class TestCompoundInterest:
    """Tests for compound interest calculation."""

    def test_compound_interest_basic(self):
        # 1000 at 10% for 1 period = 1100
        assert calculate_compound_interest(1000.0, 10.0, 1) == pytest.approx(1100.0)

    def test_compound_interest_zero_periods(self):
        assert calculate_compound_interest(1000.0, 10.0, 0) == pytest.approx(1000.0)

    # TODO: Add test for negative principal raises ValueError
    # TODO: Add test for negative rate raises ValueError
    # TODO: Add test for multiple periods (verify compounding is correct)
