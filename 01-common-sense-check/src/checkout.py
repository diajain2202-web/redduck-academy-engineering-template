# 01-common-sense-check/src/checkout.py
# A minimal order service. Fix the flaw. No framework required.

# Product catalog.
CATALOG = {
    "sku-blue-tshirt": {"name": "Blue T-shirt", "price": 2000},  # price in cents
    "sku-red-mug": {"name": "Red mug", "price": 900},
}

_orders = []


def create_order(order_id, request):
    """request = {"items": [{"productId": str, "quantity": int}, ...]}.
    Creates an order, stores it, and returns it."""
    total = 0
    items = []
    for requested_item in request["items"]:
        product_id = requested_item["productId"]
        if product_id not in CATALOG:
            raise ValueError(f"Unknown product: {product_id}")

        quantity = requested_item["quantity"]
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

        price = CATALOG[product_id]["price"]
        items.append({"productId": product_id, "quantity": quantity, "price": price})
        total += quantity * price

    order = {"id": order_id, "items": items, "total": total}
    _orders.append(order)
    return order


def get_order(order_id):
    """Look up a stored order by its id."""
    for order in _orders:
        if order["id"] == order_id:
            return order
    return None
