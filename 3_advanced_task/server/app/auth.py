from functools import wraps

from flask import current_app, jsonify, request


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Missing Authorization header."}), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header must use Bearer token."}), 401

        token = auth_header.removeprefix("Bearer ").strip()

        if not token:
            return jsonify({"error": "Admin token is missing."}), 401

        expected_token = current_app.config["ADMIN_TOKEN"]

        if token != expected_token:
            return jsonify({"error": "Unauthorized."}), 401

        return view_func(*args, **kwargs)

    return wrapper