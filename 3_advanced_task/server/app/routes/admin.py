from flask import Blueprint, jsonify

from app.auth import admin_required

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