def test_admin_check_requires_token(client):
    response = client.get("/admin/check")

    assert response.status_code == 401
    body = response.get_json()
    assert "error" in body


def test_admin_check_accepts_valid_token(client, admin_headers):
    response = client.get("/admin/check", headers=admin_headers)

    assert response.status_code == 200
    body = response.get_json()
    assert body["message"] == "Admin token is valid."


def test_add_pizza_requires_auth(client):
    response = client.post(
        "/menu",
        json={
            "name": "Quattro Formaggi",
            "price": 12.5,
            "is_available": True,
        },
    )

    assert response.status_code == 401


def test_add_pizza_success(client, admin_headers):
    response = client.post(
        "/menu",
        headers=admin_headers,
        json={
            "name": "Quattro Formaggi",
            "price": 12.5,
            "is_available": True,
        },
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body["pizza"]["name"] == "Quattro Formaggi"


def test_delete_pizza_success(client, admin_headers):
    create_response = client.post(
        "/menu",
        headers=admin_headers,
        json={
            "name": "Quattro Formaggi",
            "price": 12.5,
            "is_available": True,
        },
    )
    pizza_id = create_response.get_json()["pizza"]["id"]

    response = client.delete(f"/menu/{pizza_id}", headers=admin_headers)

    assert response.status_code == 200
    body = response.get_json()
    assert body["pizza"]["id"] == pizza_id


def test_admin_force_cancel_order_success(client, admin_headers):
    create_response = client.post(
        "/order",
        json={
            "customer_name": "Nikola",
            "address": "Novi Sad, Example 12",
            "items": [{"pizza_id": 1, "quantity": 1}],
        },
    )
    order_id = create_response.get_json()["order"]["id"]

    response = client.delete(f"/admin/order/{order_id}", headers=admin_headers)

    assert response.status_code == 200
    body = response.get_json()
    assert body["order"]["id"] == order_id
    assert body["order"]["status"] == "cancelled"