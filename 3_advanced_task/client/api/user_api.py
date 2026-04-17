import requests

from config import BASE_URL


def register_user(payload):
    response = requests.post(f"{BASE_URL}/register", json=payload, timeout=5)
    return response