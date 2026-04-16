from flask import Blueprint, jsonify

from app.db import get_db

menu_bp = Blueprint("menu", __name__)


@menu_bp.get("/menu")
def list_menu():
    db = get_db()

    pizzas = db.execute(
        """
        SELECT id, name, price, is_available
        FROM pizzas
        ORDER BY id
        """
    ).fetchall()

    result = []
    for pizza in pizzas:
        result.append(
            {
                "id": pizza["id"],
                "name": pizza["name"],
                "price": pizza["price"],
                "is_available": bool(pizza["is_available"]),
            }
        )

    return jsonify(result), 200