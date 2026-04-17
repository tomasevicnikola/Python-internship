def test_create_order_success(client):
    payload = {
        "customer_name": "Nikola",
        "address": "Novi Sad, Example 12",
        "items": [
            {"pizza_id": 1, "quantity": 2},
            {"pizza_id": 2, "quantity": 1},
        ],
    }

    response = client.post("/order", json=payload)

    assert response.status_code == 201

    body = response.get_json()
    assert body["message"] == "Order created successfully."
    assert body["order"]["customer_name"] == "Nikola"
    assert body["order"]["status"] == "created"
    assert len(body["order"]["items"]) == 2


def test_create_order_fails_for_missing_pizza(client):
    payload = {
        "customer_name": "Nikola",
        "address": "Novi Sad, Example 12",
        "items": [
            {"pizza_id": 999, "quantity": 1},
        ],
    }

    response = client.post("/order", json=payload)

    assert response.status_code == 404
    body = response.get_json()
    assert "error" in body


def test_get_order_by_id_success(client):
    create_response = client.post(
        "/order",
        json={
            "customer_name": "Nikola",
            "address": "Novi Sad, Example 12",
            "items": [{"pizza_id": 1, "quantity": 1}],
        },
    )
    order_id = create_response.get_json()["order"]["id"]

    response = client.get(f"/order/{order_id}")

    assert response.status_code == 200
    body = response.get_json()
    assert body["order"]["id"] == order_id
    assert body["order"]["status"] == "created"


def test_get_order_by_id_not_found(client):
    response = client.get("/order/999")

    assert response.status_code == 404
    body = response.get_json()
    assert "error" in body


def test_cancel_order_success(client):
    create_response = client.post(
        "/order",
        json={
            "customer_name": "Nikola",
            "address": "Novi Sad, Example 12",
            "items": [{"pizza_id": 1, "quantity": 1}],
        },
    )
    order_id = create_response.get_json()["order"]["id"]

    response = client.delete(f"/order/{order_id}")

    assert response.status_code == 200
    body = response.get_json()
    assert body["order"]["id"] == order_id
    assert body["order"]["status"] == "cancelled"


def test_cancel_order_fails_if_already_cancelled(client):
    create_response = client.post(
        "/order",
        json={
            "customer_name": "Nikola",
            "address": "Novi Sad, Example 12",
            "items": [{"pizza_id": 1, "quantity": 1}],
        },
    )
    order_id = create_response.get_json()["order"]["id"]

    client.delete(f"/order/{order_id}")
    response = client.delete(f"/order/{order_id}")

    assert response.status_code == 400
    body = response.get_json()
    assert "error" in body

def test_create_order_with_registered_user_reuses_address(client):
    register_response = client.post(
        "/register",
        json={
            "username": "nikola",
            "password": "secret123",
            "address": "Novi Sad, Saved Address 12",
        },
    )
    assert register_response.status_code == 201

    response = client.post(
        "/order",
        json={
            "username": "nikola",
            "password": "secret123",
            "items": [{"pizza_id": 1, "quantity": 2}],
        },
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body["order"]["customer_name"] == "nikola"
    assert body["order"]["address"] == "Novi Sad, Saved Address 12"
    assert body["order"]["user_id"] is not None


def test_create_order_with_registered_user_invalid_password_fails(client):
    client.post(
        "/register",
        json={
            "username": "nikola",
            "password": "secret123",
            "address": "Novi Sad, Saved Address 12",
        },
    )

    response = client.post(
        "/order",
        json={
            "username": "nikola",
            "password": "wrongpass",
            "items": [{"pizza_id": 1, "quantity": 1}],
        },
    )

    assert response.status_code == 401
    body = response.get_json()
    assert "error" in body