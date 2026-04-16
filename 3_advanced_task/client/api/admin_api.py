import requests

from config import BASE_URL


def add_pizza(token, payload):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(f"{BASE_URL}/menu", json=payload, headers=headers, timeout=5)
    return response


def delete_pizza(token, pizza_id):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(
        f"{BASE_URL}/menu/{pizza_id}",
        headers=headers,
        timeout=5,
    )
    return response


def force_cancel_order(token, order_id):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(
        f"{BASE_URL}/admin/order/{order_id}",
        headers=headers,
        timeout=5,
    )
    return response