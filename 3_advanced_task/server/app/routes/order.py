from flask import Blueprint, jsonify, request

from app.services.order_service import create_order, get_order_by_id, cancel_order


order_bp = Blueprint("order", __name__)


@order_bp.post("/order")
def create_order_route():
    """
    Create a new order
    ---
    tags:
      - Customer
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - customer_name
            - address
            - items
          properties:
            customer_name:
              type: string
              example: Nikola
            address:
              type: string
              example: Novi Sad, Example Street 12
            items:
              type: array
              items:
                type: object
                required:
                  - pizza_id
                  - quantity
                properties:
                  pizza_id:
                    type: integer
                    example: 1
                  quantity:
                    type: integer
                    example: 2
    responses:
      201:
        description: Order created successfully
      400:
        description: Invalid request data
      404:
        description: Pizza not found
    """
    data = request.get_json(silent=True)
    response_body, status_code = create_order(data)
    return jsonify(response_body), status_code

@order_bp.get("/order/<int:order_id>")
def get_order_route(order_id):
    """
    Get order status by ID
    ---
    tags:
      - Customer
    parameters:
      - in: path
        name: order_id
        type: integer
        required: true
        description: Order ID
    responses:
      200:
        description: Order retrieved successfully
      404:
        description: Order not found
    """
    response_body, status_code = get_order_by_id(order_id)
    return jsonify(response_body), status_code

@order_bp.delete("/order/<int:order_id>")
def cancel_order_route(order_id):
    """
    Cancel an order
    ---
    tags:
      - Customer
    parameters:
      - in: path
        name: order_id
        type: integer
        required: true
        description: Order ID
    responses:
      200:
        description: Order cancelled successfully
      400:
        description: Order cannot be cancelled in current status
      404:
        description: Order not found
    """
    response_body, status_code = cancel_order(order_id)
    return jsonify(response_body), status_code