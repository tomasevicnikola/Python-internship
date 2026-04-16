from flask import Flask

from app.config import Config
from app.db import init_app as init_db_app


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    init_db_app(app)

    return app