import requests

from config import BASE_URL


def add_pizza(token, payload):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(f"{BASE_URL}/menu", json=payload, headers=headers, timeout=5)
    return response