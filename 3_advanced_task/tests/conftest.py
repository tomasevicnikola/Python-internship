import os
import sys
import tempfile
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SERVER_ROOT = PROJECT_ROOT / "server"
CLIENT_ROOT = PROJECT_ROOT / "client"

sys.path.insert(0, str(SERVER_ROOT))
sys.path.insert(0, str(CLIENT_ROOT))

os.environ["ADMIN_TOKEN"] = "test-admin-token"

from app import create_app
from app.db import init_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app()
    app.config.update(
        TESTING=True,
        DATABASE_PATH=db_path,
    )

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    Path(db_path).unlink(missing_ok=True)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_headers():
    return {
        "Authorization": "Bearer test-admin-token"
    }