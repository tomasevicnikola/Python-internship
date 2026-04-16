from unittest.mock import Mock, patch

from commands.admin_commands import (
    handle_add_pizza,
    handle_delete_pizza,
    handle_force_cancel_order,
)


@patch("commands.admin_commands.add_pizza")
def test_handle_add_pizza_success(mock_add_pizza, capsys):
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "message": "Pizza added successfully.",
        "pizza": {
            "id": 5,
            "name": "Quattro Formaggi",
            "price": 12.5,
            "is_available": True,
        },
    }
    mock_add_pizza.return_value = mock_response

    handle_add_pizza("token", "Quattro Formaggi", 12.5, "true")

    captured = capsys.readouterr()
    assert "Pizza added successfully." in captured.out
    assert "Quattro Formaggi" in captured.out


@patch("commands.admin_commands.delete_pizza")
def test_handle_delete_pizza_success(mock_delete_pizza, capsys):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": "Pizza deleted successfully.",
        "pizza": {
            "id": 5,
            "name": "Quattro Formaggi",
        },
    }
    mock_delete_pizza.return_value = mock_response

    handle_delete_pizza("token", 5)

    captured = capsys.readouterr()
    assert "Pizza deleted successfully." in captured.out
    assert "Pizza ID: 5" in captured.out


@patch("commands.admin_commands.force_cancel_order")
def test_handle_force_cancel_order_success(mock_force_cancel_order, capsys):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": "Order cancelled successfully by admin.",
        "order": {
            "id": 2,
            "status": "cancelled",
        },
    }
    mock_force_cancel_order.return_value = mock_response

    handle_force_cancel_order("token", 2)

    captured = capsys.readouterr()
    assert "Order cancelled successfully by admin." in captured.out
    assert "Order ID: 2" in captured.out