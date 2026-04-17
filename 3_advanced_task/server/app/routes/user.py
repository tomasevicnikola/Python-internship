from flask import Blueprint, jsonify, request

from app.services.user_service import register_user

user_bp = Blueprint("user", __name__)


@user_bp.post("/register")
def register_user_route():
    """
    Register a new user
    ---
    tags:
      - User
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
            - address
          properties:
            username:
              type: string
              example: nikola
            password:
              type: string
              example: secret123
            address:
              type: string
              example: Novi Sad, Example Street 12
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid request data
    """
    data = request.get_json(silent=True)
    response_body, status_code = register_user(data)
    return jsonify(response_body), status_code