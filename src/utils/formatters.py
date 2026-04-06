"""Data formatting utilities."""
from typing import List
from ..models.order import Order, OrderItem
from ..models.customer import Customer


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format a monetary amount as a currency string."""
    if currency == "USD":
        return f"${amount:,.2f}"
    elif currency == "EUR":
        return f"€{amount:,.2f}"
    elif currency == "GBP":
        return f"£{amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"


def format_order_summary(order: Order) -> str:
    """Return a human-readable summary of an order."""
    lines = [
        f"Order ID: {order.id}",
        f"Status:   {order.status.value.upper()}",
        f"Items:    {order.item_count}",
        f"Subtotal: {format_currency(order.subtotal)}",
    ]
    if order.discount_amount > 0:
        lines.append(f"Discount: -{format_currency(order.discount_amount)}")
    if order.shipping_cost > 0:
        lines.append(f"Shipping: {format_currency(order.shipping_cost)}")
    lines.append(f"Total:    {format_currency(order.total)}")
    return "\n".join(lines)


def format_customer_info(customer: Customer) -> str:
    """Return a human-readable summary of a customer."""
    return (
        f"Customer: {customer.name} ({customer.id})\n"
        f"Email:    {customer.email}\n"
        f"Tier:     {customer.tier.value.upper()}\n"
        f"Spent:    {format_currency(customer.total_spent)}\n"
        f"Orders:   {customer.order_count}"
    )


def format_item_list(items: List[OrderItem]) -> str:
    """Return a formatted list of order items."""
    if not items:
        return "  (no items)"
    lines = []
    for item in items:
        lines.append(
            f"  - {item.product_name} x{item.quantity} @ {format_currency(item.unit_price)}"
            f" = {format_currency(item.subtotal)}"
        )
    return "\n".join(lines)
