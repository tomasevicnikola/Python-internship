from datetime import UTC, datetime

from app.db import get_db


def create_order(data):
    if not data:
        return {"error": "Request body must be valid JSON."}, 400

    customer_name = data.get("customer_name")
    address = data.get("address")
    items = data.get("items")

    if not customer_name or not isinstance(customer_name, str):
        return {"error": "customer_name is required and must be a string."}, 400

    if not address or not isinstance(address, str):
        return {"error": "address is required and must be a string."}, 400

    if not isinstance(items, list) or not items:
        return {"error": "items is required and must be a non-empty list."}, 400

    db = get_db()

    validated_items = []
    total_price = 0.0

    for item in items:
        if not isinstance(item, dict):
            return {"error": "Each item must be an object."}, 400

        pizza_id = item.get("pizza_id")
        quantity = item.get("quantity")

        if not isinstance(pizza_id, int):
            return {"error": "pizza_id must be an integer."}, 400

        if not isinstance(quantity, int) or quantity <= 0:
            return {"error": "quantity must be a positive integer."}, 400

        pizza = db.execute(
            """
            SELECT id, name, price, is_available
            FROM pizzas
            WHERE id = ?
            """,
            (pizza_id,),
        ).fetchone()

        if pizza is None:
            return {"error": f"Pizza with id {pizza_id} was not found."}, 404

        if not pizza["is_available"]:
            return {"error": f"Pizza '{pizza['name']}' is not available."}, 400

        unit_price = float(pizza["price"])
        item_total = unit_price * quantity
        total_price += item_total

        validated_items.append(
            {
                "pizza_id": pizza["id"],
                "pizza_name": pizza["name"],
                "quantity": quantity,
                "unit_price": unit_price,
            }
        )

    created_at = datetime.now(UTC).isoformat()
    status = "created"

    cursor = db.execute(
        """
        INSERT INTO orders (customer_name, address, status, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (customer_name, address, status, created_at),
    )

    order_id = cursor.lastrowid

    for item in validated_items:
        db.execute(
            """
            INSERT INTO order_items (order_id, pizza_id, quantity, price_at_order_time)
            VALUES (?, ?, ?, ?)
            """,
            (
                order_id,
                item["pizza_id"],
                item["quantity"],
                item["unit_price"],
            ),
        )

    db.commit()

    return (
        {
            "message": "Order created successfully.",
            "order": {
                "id": order_id,
                "customer_name": customer_name,
                "address": address,
                "status": status,
                "created_at": created_at,
                "total_price": round(total_price, 2),
                "items": validated_items,
            },
        },
        201,
    )