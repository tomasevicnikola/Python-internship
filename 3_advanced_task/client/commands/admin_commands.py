import sys
import requests

from api.admin_api import add_pizza, delete_pizza


def parse_bool(value):
    normalized = value.strip().lower()

    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False

    raise ValueError("is_available must be true or false.")


def handle_add_pizza(token, name, price, is_available_raw):
    try:
        is_available = parse_bool(is_available_raw)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    payload = {
        "name": name,
        "price": price,
        "is_available": is_available,
    }

    try:
        response = add_pizza(token, payload)
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
    pizza = body["pizza"]

    print(body["message"])
    print(f"Pizza ID: {pizza['id']}")
    print(f"Name: {pizza['name']}")
    print(f"Price: ${pizza['price']:.2f}")
    print(f"Available: {pizza['is_available']}")


def handle_delete_pizza(token, pizza_id):
    try:
        response = delete_pizza(token, pizza_id)
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
    pizza = body["pizza"]

    print(body["message"])
    print(f"Pizza ID: {pizza['id']}")
    print(f"Name: {pizza['name']}")