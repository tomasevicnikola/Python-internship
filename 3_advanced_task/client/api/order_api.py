import requests

from config import BASE_URL


def create_order(payload):
    response = requests.post(f"{BASE_URL}/order", json=payload, timeout=5)
    return response