from flask import Flask
from flasgger import Swagger

from app.config import Config
from app.db import init_app as init_db_app
from app.routes.admin import admin_bp
from app.routes.menu import menu_bp
from app.routes.order import order_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Pizza Ordering API",
            "description": "API for pizza ordering system",
            "version": "1.0.0",
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter: Bearer <your-admin-token>",
            }
        },
    }

    Swagger(app, config=swagger_config, template=swagger_template)
    init_db_app(app)

    app.register_blueprint(menu_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(admin_bp)

    return app