import sys
import requests

from api.user_api import register_user


def handle_register_user(username, password, address):
    payload = {
        "username": username,
        "password": password,
        "address": address,
    }

    try:
        response = register_user(payload)
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
    user = body["user"]

    print(body["message"])
    print(f"User ID: {user['id']}")
    print(f"Username: {user['username']}")
    print(f"Address: {user['address']}")