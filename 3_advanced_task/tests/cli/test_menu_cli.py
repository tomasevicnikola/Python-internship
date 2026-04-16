from unittest.mock import Mock, patch

from commands.menu_commands import handle_list_menu


@patch("commands.menu_commands.fetch_menu")
def test_handle_list_menu_success(mock_fetch_menu, capsys):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": 1,
            "name": "Margherita",
            "price": 8.5,
            "is_available": True,
        }
    ]
    mock_fetch_menu.return_value = mock_response

    handle_list_menu()

    captured = capsys.readouterr()
    assert "Menu:" in captured.out
    assert "Margherita" in captured.out