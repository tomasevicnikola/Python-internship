import sys
import requests

from api.order_api import create_order, get_order, cancel_order

def parse_items(raw_items):
    items = []

    for raw_item in raw_items:
        parts = raw_item.split(":")

        if len(parts) != 2:
            raise ValueError(
                f"Invalid item format '{raw_item}'. Expected format: pizza_id:quantity"
            )

        pizza_id_str, quantity_str = parts

        try:
            pizza_id = int(pizza_id_str)
            quantity = int(quantity_str)
        except ValueError as exc:
            raise ValueError(
                f"Invalid numbers in item '{raw_item}'. Expected integers."
            ) from exc

        if pizza_id <= 0 or quantity <= 0:
            raise ValueError(
                f"Invalid values in item '{raw_item}'. pizza_id and quantity must be positive."
            )

        items.append(
            {
                "pizza_id": pizza_id,
                "quantity": quantity,
            }
        )

    return items


def handle_create_order(customer_name, address, raw_items):
    try:
        items = parse_items(raw_items)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    payload = {
        "customer_name": customer_name,
        "address": address,
        "items": items,
    }

    try:
        response = create_order(payload)
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        sys.exit(1)

    if response.status_code != 201:
        try:
            error_body = response.json()
        except ValueError:
            print(f"Error: {response.status_code} - {response.text}")
            sys.exit(1)

        print(f"Error: {response.status_code} - {error_body}")
        sys.exit(1)

    body = response.json()
    order = body["order"]

    print(body["message"])
    print(f"Order ID: {order['id']}")
    print(f"Customer: {order['customer_name']}")
    print(f"Address: {order['address']}")
    print(f"Status: {order['status']}")
    print(f"Total price: ${order['total_price']:.2f}")
    print("Items:")

    for item in order["items"]:
        print(
            f"- Pizza ID {item['pizza_id']} ({item['pizza_name']}) x{item['quantity']} "
            f"@ ${item['unit_price']:.2f}"
        )

def handle_get_order(order_id):
    try:
        response = get_order(order_id)
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        sys.exit(1)

    if response.status_code != 200:
        try:
            error_body = response.json()
        except ValueError:
            print(f"Error: {response.status_code} - {response.text}")
            sys.exit(1)

        print(f"Error: {response.status_code} - {error_body}")
        sys.exit(1)

    body = response.json()
    order = body["order"]

    print(f"Order ID: {order['id']}")
    print(f"Customer: {order['customer_name']}")
    print(f"Address: {order['address']}")
    print(f"Status: {order['status']}")
    print(f"Created at: {order['created_at']}")
    print(f"Total price: ${order['total_price']:.2f}")
    print("Items:")

    for item in order["items"]:
        print(
            f"- Pizza ID {item['pizza_id']} ({item['pizza_name']}) x{item['quantity']} "
            f"@ ${item['unit_price']:.2f}"
        )

def handle_cancel_order(order_id):
    try:
        response = cancel_order(order_id)
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        sys.exit(1)

    if response.status_code != 200:
        try:
            error_body = response.json()
        except ValueError:
            print(f"Error: {response.status_code} - {response.text}")
            sys.exit(1)

        print(f"Error: {response.status_code} - {error_body}")
        sys.exit(1)

    body = response.json()
    order = body["order"]

    print(body["message"])
    print(f"Order ID: {order['id']}")
    print(f"Status: {order['status']}")