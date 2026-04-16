from flask import Blueprint, jsonify, request

from app.auth import admin_required
from app.services.menu_service import get_menu, add_pizza

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
    return jsonify(get_menu()), 200

@menu_bp.post("/menu")
@admin_required
def add_pizza_route():
    """
    Add pizza to menu
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - price
          properties:
            name:
              type: string
              example: Quattro Formaggi
            price:
              type: number
              example: 12.5
            is_available:
              type: boolean
              example: true
    responses:
      201:
        description: Pizza added successfully
      400:
        description: Invalid request data
      401:
        description: Unauthorized
    """
    data = request.get_json(silent=True)
    response_body, status_code = add_pizza(data)
    return jsonify(response_body), status_code