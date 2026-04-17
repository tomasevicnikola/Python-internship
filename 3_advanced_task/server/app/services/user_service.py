from werkzeug.security import generate_password_hash

from app.db import get_db


def register_user(data):
    if not data:
        return {"error": "Request body must be valid JSON."}, 400

    username = data.get("username")
    password = data.get("password")
    address = data.get("address")

    if not username or not isinstance(username, str):
        return {"error": "username is required and must be a string."}, 400

    if not password or not isinstance(password, str):
        return {"error": "password is required and must be a string."}, 400

    if not address or not isinstance(address, str):
        return {"error": "address is required and must be a string."}, 400

    username = username.strip()
    address = address.strip()

    if len(username) < 3:
        return {"error": "username must be at least 3 characters long."}, 400

    if len(password) < 6:
        return {"error": "password must be at least 6 characters long."}, 400

    if not address:
        return {"error": "address must not be empty."}, 400

    db = get_db()

    existing_user = db.execute(
        """
        SELECT id
        FROM users
        WHERE LOWER(username) = LOWER(?)
        """,
        (username,),
    ).fetchone()

    if existing_user is not None:
        return {"error": f"User '{username}' already exists."}, 400

    password_hash = generate_password_hash(password)

    cursor = db.execute(
        """
        INSERT INTO users (username, password_hash, address)
        VALUES (?, ?, ?)
        """,
        (username, password_hash, address),
    )
    db.commit()

    return (
        {
            "message": "User registered successfully.",
            "user": {
                "id": cursor.lastrowid,
                "username": username,
                "address": address,
            },
        },
        201,
    )