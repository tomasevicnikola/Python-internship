from flask import Flask
from flasgger import Swagger

from app.config import Config
from app.db import init_app as init_db_app
from app.routes.menu import menu_bp
from app.routes.order import order_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    Swagger(app)

    init_db_app(app)

    app.register_blueprint(menu_bp)
    app.register_blueprint(order_bp)

    return app