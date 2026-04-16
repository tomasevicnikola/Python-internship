def test_get_menu_returns_seeded_pizzas(client):
    response = client.get("/menu")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) == 4
    assert data[0]["name"] == "Margherita"
    assert "price" in data[0]
    assert "is_available" in data[0]