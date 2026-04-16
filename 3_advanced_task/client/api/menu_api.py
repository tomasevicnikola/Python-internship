import requests

from config import BASE_URL


def fetch_menu():
    response = requests.get(f"{BASE_URL}/menu", timeout=5)
    return response