from flask import Blueprint, jsonify

from app.db import get_db

menu_bp = Blueprint("menu", __name__)


@menu_bp.get("/menu")
def list_menu():
    """
    Get pizza menu
    ---
    tags:
      - Customer
    responses:
      200:
        description: List of available pizzas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              price:
                type: number
              is_available:
                type: boolean
    """
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