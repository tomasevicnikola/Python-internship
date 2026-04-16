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

def add_pizza(data):
    if not data:
        return {"error": "Request body must be valid JSON."}, 400

    name = data.get("name")
    price = data.get("price")
    is_available = data.get("is_available", True)

    if not name or not isinstance(name, str):
        return {"error": "name is required and must be a string."}, 400

    if not isinstance(price, (int, float)) or price < 0:
        return {"error": "price is required and must be a non-negative number."}, 400

    if not isinstance(is_available, bool):
        return {"error": "is_available must be a boolean."}, 400

    db = get_db()

    existing = db.execute(
        """
        SELECT id
        FROM pizzas
        WHERE LOWER(name) = LOWER(?)
        """,
        (name.strip(),),
    ).fetchone()

    if existing is not None:
        return {"error": f"Pizza '{name}' already exists."}, 400

    cursor = db.execute(
        """
        INSERT INTO pizzas (name, price, is_available)
        VALUES (?, ?, ?)
        """,
        (name.strip(), float(price), int(is_available)),
    )
    db.commit()

    return (
        {
            "message": "Pizza added successfully.",
            "pizza": {
                "id": cursor.lastrowid,
                "name": name.strip(),
                "price": float(price),
                "is_available": is_available,
            },
        },
        201,
    )
def delete_pizza(pizza_id):
    db = get_db()

    pizza = db.execute(
        """
        SELECT id, name
        FROM pizzas
        WHERE id = ?
        """,
        (pizza_id,),
    ).fetchone()

    if pizza is None:
        return {"error": f"Pizza with id {pizza_id} was not found."}, 404

    db.execute(
        """
        DELETE FROM pizzas
        WHERE id = ?
        """,
        (pizza_id,),
    )
    db.commit()

    return {
        "message": "Pizza deleted successfully.",
        "pizza": {
            "id": pizza["id"],
            "name": pizza["name"],
        },
    }, 200