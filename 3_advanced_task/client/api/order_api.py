import requests

from config import BASE_URL


def create_order(payload):
    response = requests.post(f"{BASE_URL}/order", json=payload, timeout=5)
    return response

def get_order(order_id):
    response = requests.get(f"{BASE_URL}/order/{order_id}", timeout=5)
    return response

def cancel_order(order_id):
    response = requests.delete(f"{BASE_URL}/order/{order_id}", timeout=5)
    return response