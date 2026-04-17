def test_register_user_success(client):
    response = client.post(
        "/register",
        json={
            "username": "nikola",
            "password": "secret123",
            "address": "Novi Sad, Example 12",
        },
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body["message"] == "User registered successfully."
    assert body["user"]["username"] == "nikola"
    assert body["user"]["address"] == "Novi Sad, Example 12"


def test_register_user_duplicate_username_fails(client):
    client.post(
        "/register",
        json={
            "username": "nikola",
            "password": "secret123",
            "address": "Novi Sad, Example 12",
        },
    )

    response = client.post(
        "/register",
        json={
            "username": "nikola",
            "password": "another123",
            "address": "Belgrade, Example 5",
        },
    )

    assert response.status_code == 400
    body = response.get_json()
    assert "error" in body


def test_register_user_short_username_fails(client):
    response = client.post(
        "/register",
        json={
            "username": "ab",
            "password": "secret123",
            "address": "Novi Sad, Example 12",
        },
    )

    assert response.status_code == 400
    body = response.get_json()
    assert "error" in body


def test_register_user_short_password_fails(client):
    response = client.post(
        "/register",
        json={
            "username": "nikola",
            "password": "123",
            "address": "Novi Sad, Example 12",
        },
    )

    assert response.status_code == 400
    body = response.get_json()
    assert "error" in body