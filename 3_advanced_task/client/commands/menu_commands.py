import sys
import requests

from api.menu_api import fetch_menu


def handle_list_menu():
    try:
        response = fetch_menu()
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        sys.exit(1)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        sys.exit(1)

    pizzas = response.json()

    if not pizzas:
        print("Menu is empty.")
        return

    print("Menu:")
    for pizza in pizzas:
        availability = "available" if pizza["is_available"] else "unavailable"
        print(
            f"- [{pizza['id']}] {pizza['name']} | "
            f"${pizza['price']:.2f} | {availability}"
        )