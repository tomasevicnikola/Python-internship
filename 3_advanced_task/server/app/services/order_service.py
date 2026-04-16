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

def get_order_by_id(order_id):
    db = get_db()

    order = db.execute(
        """
        SELECT id, customer_name, address, status, created_at
        FROM orders
        WHERE id = ?
        """,
        (order_id,),
    ).fetchone()

    if order is None:
        return {"error": f"Order with id {order_id} was not found."}, 404

    items = db.execute(
        """
        SELECT
            oi.pizza_id,
            p.name AS pizza_name,
            oi.quantity,
            oi.price_at_order_time
        FROM order_items oi
        JOIN pizzas p ON p.id = oi.pizza_id
        WHERE oi.order_id = ?
        ORDER BY oi.id
        """,
        (order_id,),
    ).fetchall()

    serialized_items = []
    total_price = 0.0

    for item in items:
        unit_price = float(item["price_at_order_time"])
        quantity = item["quantity"]
        total_price += unit_price * quantity

        serialized_items.append(
            {
                "pizza_id": item["pizza_id"],
                "pizza_name": item["pizza_name"],
                "quantity": quantity,
                "unit_price": unit_price,
            }
        )

    return (
        {
            "order": {
                "id": order["id"],
                "customer_name": order["customer_name"],
                "address": order["address"],
                "status": order["status"],
                "created_at": order["created_at"],
                "total_price": round(total_price, 2),
                "items": serialized_items,
            }
        },
        200,
    )

def cancel_order(order_id):
    db = get_db()

    order = db.execute(
        """
        SELECT id, status
        FROM orders
        WHERE id = ?
        """,
        (order_id,),
    ).fetchone()

    if order is None:
        return {"error": f"Order with id {order_id} was not found."}, 404

    current_status = order["status"]

    forbidden_statuses = {"ready_to_be_delivered", "delivered", "cancelled"}

    if current_status in forbidden_statuses:
        return {
            "error": f"Order cannot be cancelled because its status is '{current_status}'."
        }, 400

    new_status = "cancelled"

    db.execute(
        """
        UPDATE orders
        SET status = ?
        WHERE id = ?
        """,
        (new_status, order_id),
    )
    db.commit()

    return {
        "message": "Order cancelled successfully.",
        "order": {
            "id": order_id,
            "status": new_status,
        },
    }, 200