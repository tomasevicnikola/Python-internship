from flask import Blueprint, jsonify

from app.auth import admin_required
from app.services.order_service import admin_cancel_order

admin_bp = Blueprint("admin", __name__)


@admin_bp.get("/admin/check")
@admin_required
def admin_check():
    """
    Verify admin token
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: Admin token is valid
      401:
        description: Unauthorized
    """
    return jsonify({"message": "Admin token is valid."}), 200


@admin_bp.delete("/admin/order/<int:order_id>")
@admin_required
def admin_cancel_order_route(order_id):
    """
    Force-cancel an order
    ---
    tags:
      - Admin
    security:
      - Bearer: []
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
        description: Order already cancelled
      401:
        description: Unauthorized
      404:
        description: Order not found
    """
    response_body, status_code = admin_cancel_order(order_id)
    return jsonify(response_body), status_code