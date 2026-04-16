from app.db import get_db


def get_menu():
    db = get_db()

    pizzas = db.execute(
        """
        SELECT id, name, price, is_available
        FROM pizzas
        ORDER BY id
        """
    ).fetchall()

    return [
        {
            "id": pizza["id"],
            "name": pizza["name"],
            "price": pizza["price"],
            "is_available": bool(pizza["is_available"]),
        }
        for pizza in pizzas
    ]