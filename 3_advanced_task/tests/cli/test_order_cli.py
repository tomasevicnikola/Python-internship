from unittest.mock import Mock, patch

from commands.order_commands import (
    handle_cancel_order,
    handle_create_order,
    handle_get_order,
)


@patch("commands.order_commands.create_order")
def test_handle_create_order_success(mock_create_order, capsys):
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "message": "Order created successfully.",
        "order": {
            "id": 1,
            "customer_name": "Nikola",
            "address": "Novi Sad, Example 12",
            "status": "created",
            "total_price": 27.0,
            "items": [
                {
                    "pizza_id": 1,
                    "pizza_name": "Margherita",
                    "quantity": 2,
                    "unit_price": 8.5,
                }
            ],
        },
    }
    mock_create_order.return_value = mock_response

    handle_create_order(
        raw_items=["1:2"],
        customer_name="Nikola",
        address="Novi Sad, Example 12",
    )

    captured = capsys.readouterr()
    assert "Order created successfully." in captured.out
    assert "Order ID: 1" in captured.o


@patch("commands.order_commands.get_order")
def test_handle_get_order_success(mock_get_order, capsys):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "order": {
            "id": 1,
            "customer_name": "Nikola",
            "address": "Novi Sad, Example 12",
            "status": "created",
            "created_at": "2026-04-16T11:25:18+00:00",
            "total_price": 27.0,
            "items": [
                {
                    "pizza_id": 1,
                    "pizza_name": "Margherita",
                    "quantity": 2,
                    "unit_price": 8.5,
                }
            ],
        }
    }
    mock_get_order.return_value = mock_response

    handle_get_order(1)

    captured = capsys.readouterr()
    assert "Order ID: 1" in captured.out
    assert "Status: created" in captured.out


@patch("commands.order_commands.cancel_order")
def test_handle_cancel_order_success(mock_cancel_order, capsys):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": "Order cancelled successfully.",
        "order": {
            "id": 1,
            "status": "cancelled",
        },
    }
    mock_cancel_order.return_value = mock_response

    handle_cancel_order(1)

    captured = capsys.readouterr()
    assert "Order cancelled successfully." in captured.out
    assert "Status: cancelled" in captured.out


@patch("commands.order_commands.create_order")
def test_handle_create_order_with_registered_user_success(mock_create_order, capsys):
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "message": "Order created successfully.",
        "order": {
            "id": 2,
            "customer_name": "nikola",
            "address": "Novi Sad, Saved Address 12",
            "status": "created",
            "total_price": 17.0,
            "items": [
                {
                    "pizza_id": 1,
                    "pizza_name": "Margherita",
                    "quantity": 2,
                    "unit_price": 8.5,
                }
            ],
        },
    }
    mock_create_order.return_value = mock_response

    handle_create_order(
        raw_items=["1:2"],
        username="nikola",
        password="secret123",
    )

    captured = capsys.readouterr()
    assert "Order created successfully." in captured.out
    assert "Customer: nikola" in captured.out
    assert "Novi Sad, Saved Address 12" in captured.out