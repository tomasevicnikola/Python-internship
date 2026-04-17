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
    assert body["user"]["username"] == "nikola"


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