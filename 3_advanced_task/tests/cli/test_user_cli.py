from unittest.mock import Mock, patch

from commands.user_commands import handle_register_user


@patch("commands.user_commands.register_user")
def test_handle_register_user_success(mock_register_user, capsys):
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "message": "User registered successfully.",
        "user": {
            "id": 1,
            "username": "nikola",
            "address": "Novi Sad, Example 12",
        },
    }
    mock_register_user.return_value = mock_response

    handle_register_user("nikola", "secret123", "Novi Sad, Example 12")

    captured = capsys.readouterr()
    assert "User registered successfully." in captured.out
    assert "Username: nikola" in captured.out